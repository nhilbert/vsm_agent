#!/usr/bin/env python3
"""
VSG Telegram Long-Polling Daemon

Continuously polls Telegram for new messages using long polling (timeout=30s).
Writes incoming messages to .telegram_incoming for the cycle watcher to detect.
Filters by VSG_TELEGRAM_CHAT_ID so only Norman's messages are processed.

This is a dumb transducer — it converts Telegram events to file-system events.
It does not know about cycles, VSM, or anything else.

Run as a systemd service (vsg-telegram-poller.service) or manually for testing.
"""

import atexit
import json
import os
import signal
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

# Add script directory to path so we can import vsg_telegram
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from vsg_telegram import api_call, extract_message

# --- Paths ---
OFFSET_FILE = os.path.join(SCRIPT_DIR, ".telegram_offset")
INCOMING_FILE = os.path.join(SCRIPT_DIR, ".telegram_incoming")
PID_FILE = os.path.join(SCRIPT_DIR, ".telegram_poller.pid")

POLL_TIMEOUT = 120  # seconds — Telegram long-poll duration
RETRY_DELAY = 5    # seconds — delay after API failure


def log(msg):
    """Log with timestamp to stderr (systemd captures this)."""
    ts = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    print(f"[{ts}] {msg}", file=sys.stderr, flush=True)


def load_env():
    """Load .env file if present."""
    env_path = os.path.join(SCRIPT_DIR, ".env")
    if os.path.exists(env_path):
        with open(env_path, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, _, value = line.partition("=")
                    key = key.strip()
                    value = value.strip().strip("'\"")
                    os.environ.setdefault(key, value)


def get_config():
    """Read bot token and chat ID from environment."""
    token = os.environ.get("VSG_TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("VSG_TELEGRAM_CHAT_ID")
    if not token:
        log("FATAL: VSG_TELEGRAM_BOT_TOKEN not set.")
        sys.exit(1)
    if not chat_id:
        log("FATAL: VSG_TELEGRAM_CHAT_ID not set.")
        sys.exit(1)
    return token, int(chat_id)


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


def write_pid():
    """Write PID file on startup."""
    with open(PID_FILE, "w") as f:
        f.write(str(os.getpid()))
    log(f"PID file written: {PID_FILE} (pid={os.getpid()})")


def remove_pid():
    """Remove PID file on exit."""
    try:
        os.remove(PID_FILE)
        log("PID file removed.")
    except OSError:
        pass


def append_incoming(lines):
    """Append message lines to .telegram_incoming (atomic-ish append)."""
    with open(INCOMING_FILE, "a") as f:
        for line in lines:
            f.write(line + "\n")


def long_poll(token, expected_chat_id):
    """Main long-polling loop. Runs forever."""
    offset = load_offset()
    log(f"Starting long-poll loop (offset={offset}, chat_id={expected_chat_id})")

    while True:
        params = {"timeout": POLL_TIMEOUT}
        if offset is not None:
            params["offset"] = offset + 1

        try:
            url = f"https://api.telegram.org/bot{token}/getUpdates"
            data = urllib.parse.urlencode(params).encode("utf-8")
            req = urllib.request.Request(url, data=data)
            # timeout = poll_timeout + 10s buffer for network
            with urllib.request.urlopen(req, timeout=POLL_TIMEOUT + 10) as resp:
                result = json.loads(resp.read().decode("utf-8"))
        except (urllib.error.URLError, urllib.error.HTTPError, OSError) as e:
            log(f"API error: {e} — retrying in {RETRY_DELAY}s")
            time.sleep(RETRY_DELAY)
            continue
        except Exception as e:
            log(f"Unexpected error: {e} — retrying in {RETRY_DELAY}s")
            time.sleep(RETRY_DELAY)
            continue

        if not result.get("ok"):
            log(f"API returned ok=false: {result} — retrying in {RETRY_DELAY}s")
            time.sleep(RETRY_DELAY)
            continue

        updates = result.get("result", [])
        if not updates:
            continue  # Normal — long poll timed out with no new messages

        incoming_lines = []
        max_update_id = offset or 0

        for update in updates:
            update_id = update.get("update_id", 0)
            if update_id > max_update_id:
                max_update_id = update_id

            msg = update.get("message")
            if not msg:
                continue

            chat_id = msg.get("chat", {}).get("id")
            if chat_id != expected_chat_id:
                from_user = msg.get("from", {}).get("first_name", "?")
                log(f"Ignoring message from chat_id={chat_id} (user={from_user}) — not Norman")
                continue

            entry = extract_message(token, msg, update_id)
            if entry:
                line = f"[{update_id}] {entry['from']}: {entry['text']}"
                incoming_lines.append(line)
                log(f"Message received: {line[:120]}")

        # Write to incoming file before advancing offset
        if incoming_lines:
            append_incoming(incoming_lines)
            log(f"Wrote {len(incoming_lines)} message(s) to {INCOMING_FILE}")

        # Advance offset
        if max_update_id > (offset or 0):
            save_offset(max_update_id)
            offset = max_update_id


def main():
    load_env()
    token, expected_chat_id = get_config()

    write_pid()
    atexit.register(remove_pid)

    # Handle signals gracefully — atexit runs on clean exit
    def handle_signal(signum, frame):
        log(f"Received signal {signum}, shutting down.")
        sys.exit(0)

    signal.signal(signal.SIGTERM, handle_signal)
    signal.signal(signal.SIGINT, handle_signal)

    log("VSG Telegram Poller starting")
    log(f"Token: ...{token[-8:]}, Chat ID: {expected_chat_id}")

    long_poll(token, expected_chat_id)


if __name__ == "__main__":
    main()
