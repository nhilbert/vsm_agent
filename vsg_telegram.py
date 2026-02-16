#!/usr/bin/env python3
"""
VSG Telegram — Send and receive messages for the Viable System Generator.

Security:
    Bot token and chat ID are read from environment variables.
    NEVER hardcode credentials. NEVER commit secrets to git.

Bot: @vsg_agent_bot
Channel: Private chat with Norman Hilbert

Usage:
    # Send a message
    python3 vsg_telegram.py send "Hello from the VSG"

    # Send from a file
    python3 vsg_telegram.py send --file message.txt

    # Check for new messages (since last check)
    python3 vsg_telegram.py check

    # Read recent messages (last N)
    python3 vsg_telegram.py read [--limit 10]

    # Test connection
    python3 vsg_telegram.py test
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.parse
import urllib.error

# --- Configuration (from environment) ---
def get_config():
    """Read bot token and chat ID from environment."""
    token = os.environ.get("VSG_TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("VSG_TELEGRAM_CHAT_ID")
    if not token:
        print("ERROR: VSG_TELEGRAM_BOT_TOKEN not set.")
        print("Set it: export VSG_TELEGRAM_BOT_TOKEN='your-token'")
        sys.exit(1)
    if not chat_id:
        print("ERROR: VSG_TELEGRAM_CHAT_ID not set.")
        print("Set it: export VSG_TELEGRAM_CHAT_ID='your-chat-id'")
        sys.exit(1)
    return token, chat_id


def api_call(token, method, params=None):
    """Call Telegram Bot API."""
    url = f"https://api.telegram.org/bot{token}/{method}"
    if params:
        data = urllib.parse.urlencode(params).encode("utf-8")
    else:
        data = None
    try:
        req = urllib.request.Request(url, data=data)
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        print(f"ERROR: HTTP {e.code}: {body}")
        return None
    except Exception as e:
        print(f"ERROR: {e}")
        return None


# --- Offset tracking (persistent last-read marker) ---
OFFSET_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".telegram_offset")


def load_offset():
    """Load the last processed update_id."""
    if os.path.exists(OFFSET_FILE):
        with open(OFFSET_FILE, "r") as f:
            try:
                return int(f.read().strip())
            except ValueError:
                return None
    return None


def save_offset(offset):
    """Save the last processed update_id."""
    with open(OFFSET_FILE, "w") as f:
        f.write(str(offset))


# --- Send ---
def send_message(text):
    """Send a message to Norman."""
    token, chat_id = get_config()
    # Telegram max message length is 4096
    if len(text) > 4096:
        # Split into chunks
        chunks = [text[i:i+4096] for i in range(0, len(text), 4096)]
        for i, chunk in enumerate(chunks):
            result = api_call(token, "sendMessage", {
                "chat_id": chat_id,
                "text": chunk,
                "parse_mode": "Markdown",
            })
            if not result or not result.get("ok"):
                # Retry without Markdown if parse fails
                result = api_call(token, "sendMessage", {
                    "chat_id": chat_id,
                    "text": chunk,
                })
            if result and result.get("ok"):
                print(f"OK: Chunk {i+1}/{len(chunks)} sent.")
            else:
                print(f"FAIL: Chunk {i+1}/{len(chunks)} failed.")
                return False
        return True
    else:
        result = api_call(token, "sendMessage", {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "Markdown",
        })
        if not result or not result.get("ok"):
            # Retry without Markdown if parse fails
            result = api_call(token, "sendMessage", {
                "chat_id": chat_id,
                "text": text,
            })
        if result and result.get("ok"):
            print("OK: Message sent.")
            return True
        else:
            print("FAIL: Message not sent.")
            return False


# --- Check for new messages ---
def check_messages():
    """Check for new messages since last check."""
    token, _ = get_config()
    offset = load_offset()
    params = {"timeout": 0}
    if offset:
        params["offset"] = offset + 1

    result = api_call(token, "getUpdates", params)
    if not result or not result.get("ok"):
        print("ERROR: Could not get updates.")
        return []

    updates = result.get("result", [])
    if not updates:
        print("No new messages.")
        return []

    messages = []
    max_update_id = offset or 0
    for update in updates:
        update_id = update.get("update_id", 0)
        if update_id > max_update_id:
            max_update_id = update_id
        msg = update.get("message")
        if msg and msg.get("text"):
            from_user = msg.get("from", {})
            name = from_user.get("first_name", "Unknown")
            text = msg["text"]
            date = msg.get("date", 0)
            messages.append({
                "from": name,
                "text": text,
                "date": date,
                "update_id": update_id,
            })
            print(f"  [{update_id}] {name}: {text}")

    if max_update_id > (offset or 0):
        save_offset(max_update_id)

    if not messages:
        print("No text messages in updates.")

    return messages


# --- Read recent messages ---
def read_messages(limit=10):
    """Read recent messages (does NOT advance the offset)."""
    token, _ = get_config()
    result = api_call(token, "getUpdates", {"timeout": 0})
    if not result or not result.get("ok"):
        print("ERROR: Could not get updates.")
        return []

    updates = result.get("result", [])
    messages = []
    for update in updates:
        msg = update.get("message")
        if msg and msg.get("text"):
            from_user = msg.get("from", {})
            name = from_user.get("first_name", "Unknown")
            text = msg["text"]
            date = msg.get("date", 0)
            messages.append({
                "from": name,
                "text": text,
                "date": date,
            })

    # Most recent last, show last N
    messages = messages[-limit:]
    if not messages:
        print("No messages.")
    else:
        for m in messages:
            print(f"  {m['from']}: {m['text']}")

    return messages


# --- Test ---
def test_connection():
    """Test Telegram bot connection."""
    token, chat_id = get_config()
    print(f"Bot token: ...{token[-8:]}")
    print(f"Chat ID: {chat_id}")
    print()

    print("Testing bot identity...")
    result = api_call(token, "getMe")
    if result and result.get("ok"):
        bot = result["result"]
        print(f"  Bot: @{bot.get('username')} ({bot.get('first_name')})")
    else:
        print("  FAIL: Could not reach bot API.")
        return False

    print("Testing send...")
    result = api_call(token, "sendMessage", {
        "chat_id": chat_id,
        "text": "VSG Telegram test — connection verified.",
    })
    if result and result.get("ok"):
        print("  Send: OK")
    else:
        print("  Send: FAIL")
        return False

    print()
    print("All tests passed. Telegram is operational.")
    return True


# --- CLI ---
def main():
    parser = argparse.ArgumentParser(description="VSG Telegram — send and receive messages")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # send
    send_parser = subparsers.add_parser("send", help="Send a message")
    send_parser.add_argument("text", nargs="?", help="Message text")
    send_parser.add_argument("--file", help="Read message from file")

    # check
    subparsers.add_parser("check", help="Check for new messages since last check")

    # read
    read_parser = subparsers.add_parser("read", help="Read recent messages")
    read_parser.add_argument("--limit", type=int, default=10, help="Number of messages")

    # test
    subparsers.add_parser("test", help="Test connection")

    args = parser.parse_args()

    if args.command == "send":
        if args.file:
            with open(args.file, "r") as f:
                text = f.read()
        elif args.text:
            text = args.text
        else:
            print("ERROR: Provide message text or --file")
            sys.exit(1)
        success = send_message(text)
        sys.exit(0 if success else 1)

    elif args.command == "check":
        check_messages()

    elif args.command == "read":
        read_messages(limit=args.limit)

    elif args.command == "test":
        success = test_connection()
        sys.exit(0 if success else 1)

    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
