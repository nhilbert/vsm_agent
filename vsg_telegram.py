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

    # Send a voice message (text-to-speech via OpenAI TTS)
    python3 vsg_telegram.py voice "Hallo, hier spricht der VSG."

    # Send a voice message from an existing audio file
    python3 vsg_telegram.py voice --file audio.ogg

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


# --- Voice message handling ---
VOICE_CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".cache", "voice")


def download_telegram_file(token, file_id):
    """Download a file from Telegram using getFile API. Returns local path or None."""
    result = api_call(token, "getFile", {"file_id": file_id})
    if not result or not result.get("ok"):
        return None
    file_path = result["result"].get("file_path")
    if not file_path:
        return None

    url = f"https://api.telegram.org/file/bot{token}/{file_path}"
    os.makedirs(VOICE_CACHE, exist_ok=True)
    ext = os.path.splitext(file_path)[1] or ".ogg"
    local_path = os.path.join(VOICE_CACHE, f"{file_id}{ext}")

    try:
        urllib.request.urlretrieve(url, local_path)
        return local_path
    except Exception as e:
        print(f"ERROR downloading file: {e}")
        return None


def transcribe_voice(file_path):
    """Transcribe a voice file. Tries OpenAI Whisper API if OPENAI_API_KEY is set."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return None

    # Multipart form upload via urllib (no external packages)
    boundary = "----VsgVoiceBoundary"
    filename = os.path.basename(file_path)
    with open(file_path, "rb") as f:
        file_data = f.read()

    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="model"\r\n\r\n'
        f"whisper-1\r\n"
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="file"; filename="{filename}"\r\n'
        f"Content-Type: audio/ogg\r\n\r\n"
    ).encode("utf-8") + file_data + f"\r\n--{boundary}--\r\n".encode("utf-8")

    req = urllib.request.Request(
        "https://api.openai.com/v1/audio/transcriptions",
        data=body,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": f"multipart/form-data; boundary={boundary}",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            return result.get("text")
    except Exception as e:
        print(f"WARNING: Whisper transcription failed: {e}")
        return None


def extract_message(token, msg, update_id=None):
    """Extract a message dict from a Telegram message object. Handles text, voice, audio, photo, and document."""
    from_user = msg.get("from", {})
    name = from_user.get("first_name", "Unknown")
    date = msg.get("date", 0)

    # Text message
    if msg.get("text"):
        entry = {"from": name, "text": msg["text"], "date": date, "type": "text"}
        if update_id is not None:
            entry["update_id"] = update_id
        return entry

    # Voice message
    voice = msg.get("voice")
    if voice:
        duration = voice.get("duration", 0)
        file_id = voice.get("file_id")
        text = f"[Voice message, {duration}s]"

        # Try to download and transcribe
        if file_id:
            local_path = download_telegram_file(token, file_id)
            if local_path:
                transcript = transcribe_voice(local_path)
                if transcript:
                    text = f"[Voice, {duration}s] {transcript}"
                else:
                    text = f"[Voice message, {duration}s — no transcription available. File saved: {local_path}]"

        entry = {"from": name, "text": text, "date": date, "type": "voice"}
        if update_id is not None:
            entry["update_id"] = update_id
        return entry

    # Audio message (voice notes sent as audio files)
    audio = msg.get("audio")
    if audio:
        duration = audio.get("duration", 0)
        title = audio.get("title", "untitled")
        entry = {"from": name, "text": f"[Audio: {title}, {duration}s]", "date": date, "type": "audio"}
        if update_id is not None:
            entry["update_id"] = update_id
        return entry

    # Photo message
    photos = msg.get("photo")
    if photos:
        # Telegram sends multiple sizes; pick the largest (last in array)
        largest = photos[-1]
        file_id = largest.get("file_id")
        width = largest.get("width", 0)
        height = largest.get("height", 0)
        caption = msg.get("caption", "")
        text = f"[Photo, {width}x{height}]"

        if file_id:
            local_path = download_telegram_file(token, file_id)
            if local_path:
                text = f"[Photo, {width}x{height}, saved: {local_path}]"
            else:
                text = f"[Photo, {width}x{height}, download failed]"

        if caption:
            text += f" Caption: {caption}"

        entry = {"from": name, "text": text, "date": date, "type": "photo"}
        if update_id is not None:
            entry["update_id"] = update_id
        return entry

    # Document/file message
    document = msg.get("document")
    if document:
        file_name = document.get("file_name", "unknown")
        mime_type = document.get("mime_type", "")
        caption = msg.get("caption", "")
        text = f"[Document: {file_name} ({mime_type})]"
        if caption:
            text += f" Caption: {caption}"
        entry = {"from": name, "text": text, "date": date, "type": "document"}
        if update_id is not None:
            entry["update_id"] = update_id
        return entry

    return None


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


# --- Text-to-Speech ---
def generate_tts(text, output_path=None, voice="onyx", model="tts-1-hd"):
    """Generate speech from text using OpenAI TTS. Returns path to .ogg file or None."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("ERROR: OPENAI_API_KEY not set. Required for TTS.")
        return None

    payload = json.dumps({
        "model": model,
        "input": text,
        "voice": voice,
        "response_format": "opus",
    }).encode("utf-8")

    req = urllib.request.Request(
        "https://api.openai.com/v1/audio/speech",
        data=payload,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            audio_data = resp.read()
            if not output_path:
                os.makedirs(VOICE_CACHE, exist_ok=True)
                output_path = os.path.join(VOICE_CACHE, "tts_output.ogg")
            with open(output_path, "wb") as f:
                f.write(audio_data)
            print(f"OK: TTS generated ({len(audio_data)} bytes) -> {output_path}")
            return output_path
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")[:500]
        print(f"ERROR: TTS failed (HTTP {e.code}): {body}")
        return None
    except Exception as e:
        print(f"ERROR: TTS failed: {e}")
        return None


# --- Send Voice ---
def send_voice(file_path):
    """Send a voice message (.ogg) to Norman via Telegram."""
    token, chat_id = get_config()

    with open(file_path, "rb") as f:
        file_data = f.read()

    boundary = "VsgVoiceSendBoundary"
    filename = os.path.basename(file_path)

    parts = []
    parts.append(
        "--{b}\r\n"
        "Content-Disposition: form-data; name=\"chat_id\"\r\n\r\n"
        "{v}\r\n".format(b=boundary, v=chat_id).encode("utf-8")
    )
    parts.append(
        "--{b}\r\n"
        "Content-Disposition: form-data; name=\"voice\"; filename=\"{fn}\"\r\n"
        "Content-Type: audio/ogg\r\n\r\n".format(b=boundary, fn=filename).encode("utf-8")
    )
    parts.append(file_data)
    parts.append("\r\n--{b}--\r\n".format(b=boundary).encode("utf-8"))

    body = b"".join(parts)

    req = urllib.request.Request(
        "https://api.telegram.org/bot{t}/sendVoice".format(t=token),
        data=body,
        headers={
            "Content-Type": "multipart/form-data; boundary={b}".format(b=boundary),
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            if result.get("ok"):
                voice_info = result["result"].get("voice", {})
                duration = voice_info.get("duration", "?")
                print(f"OK: Voice message sent ({duration}s).")
                return True
            else:
                print(f"FAIL: API returned ok=false: {result}")
                return False
    except urllib.error.HTTPError as e:
        body_resp = e.read().decode("utf-8", errors="replace")[:500]
        print(f"ERROR: HTTP {e.code}: {body_resp}")
        return False
    except Exception as e:
        print(f"ERROR: {e}")
        return False


# --- Check for new messages ---
def check_messages():
    """Check for new messages since last check. Filters by expected chat_id."""
    token, expected_chat_id = get_config()
    expected_chat_id = int(expected_chat_id)
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
        if msg:
            chat_id = msg.get("chat", {}).get("id")
            if chat_id != expected_chat_id:
                print(f"  [{update_id}] Ignoring message from chat_id={chat_id} (not expected)")
                continue
            entry = extract_message(token, msg, update_id)
            if entry:
                messages.append(entry)
                print(f"  [{update_id}] {entry['from']}: {entry['text']}")

    if max_update_id > (offset or 0):
        save_offset(max_update_id)

    if not messages:
        print("No messages in updates.")

    return messages


# --- Read recent messages ---
def read_messages(limit=10):
    """Read recent messages (does NOT advance the offset). Filters by expected chat_id."""
    token, expected_chat_id = get_config()
    expected_chat_id = int(expected_chat_id)
    result = api_call(token, "getUpdates", {"timeout": 0})
    if not result or not result.get("ok"):
        print("ERROR: Could not get updates.")
        return []

    updates = result.get("result", [])
    messages = []
    for update in updates:
        msg = update.get("message")
        if msg:
            chat_id = msg.get("chat", {}).get("id")
            if chat_id != expected_chat_id:
                continue
            entry = extract_message(token, msg)
            if entry:
                messages.append(entry)

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
    send_parser = subparsers.add_parser("send", help="Send a text message")
    send_parser.add_argument("text", nargs="?", help="Message text")
    send_parser.add_argument("--file", help="Read message from file")

    # voice
    voice_parser = subparsers.add_parser("voice", help="Send a voice message (TTS or file)")
    voice_parser.add_argument("text", nargs="?", help="Text to convert to speech")
    voice_parser.add_argument("--file", help="Send existing .ogg audio file")
    voice_parser.add_argument("--voice", default="onyx", help="TTS voice (default: onyx)")

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

    elif args.command == "voice":
        if args.file:
            success = send_voice(args.file)
        elif args.text:
            ogg_path = generate_tts(args.text, voice=args.voice)
            if ogg_path:
                success = send_voice(ogg_path)
            else:
                success = False
        else:
            print("ERROR: Provide text for TTS or --file with an .ogg file")
            sys.exit(1)
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
