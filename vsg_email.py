#!/usr/bin/env python3
"""
VSG Email — Send and receive email for the Viable System Generator.

Security:
    Password is read from environment variable VSG_EMAIL_PASSWORD.
    NEVER hardcode credentials. NEVER commit secrets to git.

Provider: Ionos Deutschland
Address: vsg-agent@nhilbert.de

Usage:
    # Send an email
    python3 vsg_email.py send --to "recipient@example.com" --subject "Subject" --body "Message body"

    # Send from a file (body is file content)
    python3 vsg_email.py send --to "recipient@example.com" --subject "Subject" --body-file message.txt

    # Check inbox (list recent messages)
    python3 vsg_email.py check [--limit 10]

    # Read a specific email by index (1-based, most recent first)
    python3 vsg_email.py read --index 1

    # Test connection
    python3 vsg_email.py test
"""

import argparse
import email
import imaplib
import os
import smtplib
import ssl
import sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import decode_header
from datetime import datetime

# --- Configuration (non-secret) ---
EMAIL_ADDRESS = "vsg-agent@nhilbert.de"
SMTP_SERVER = "smtp.ionos.com"
SMTP_PORT = 465  # SSL/TLS
IMAP_SERVER = "imap.ionos.com"
IMAP_PORT = 993  # SSL/TLS

# --- Credential retrieval ---
def get_password():
    """Read password from environment. Never hardcode."""
    pw = os.environ.get("VSG_EMAIL_PASSWORD")
    if not pw:
        print("ERROR: VSG_EMAIL_PASSWORD environment variable not set.")
        print("Set it before running: export VSG_EMAIL_PASSWORD='your-password'")
        sys.exit(1)
    return pw


# --- Send ---
def send_email(to_address, subject, body, reply_to=None):
    """Send an email via SMTP over SSL."""
    password = get_password()

    msg = MIMEMultipart()
    msg["From"] = f"VSG Agent <{EMAIL_ADDRESS}>"
    msg["To"] = to_address
    msg["Subject"] = subject
    msg["Date"] = email.utils.formatdate(localtime=True)
    if reply_to:
        msg["Reply-To"] = reply_to

    msg.attach(MIMEText(body, "plain", "utf-8"))

    context = ssl.create_default_context()

    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context, timeout=30) as server:
            server.login(EMAIL_ADDRESS, password)
            server.send_message(msg)
        print(f"OK: Email sent to {to_address}")
        print(f"    Subject: {subject}")
        return True
    except smtplib.SMTPAuthenticationError:
        print("ERROR: Authentication failed. Check VSG_EMAIL_PASSWORD.")
        return False
    except smtplib.SMTPException as e:
        print(f"ERROR: SMTP error: {e}")
        return False
    except Exception as e:
        print(f"ERROR: {e}")
        return False


# --- Check inbox ---
def check_inbox(limit=10):
    """List recent emails from IMAP inbox."""
    password = get_password()
    context = ssl.create_default_context()

    try:
        with imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT, ssl_context=context) as mail:
            mail.login(EMAIL_ADDRESS, password)
            mail.select("INBOX", readonly=True)

            status, messages = mail.search(None, "ALL")
            if status != "OK":
                print("ERROR: Could not search inbox.")
                return []

            msg_ids = messages[0].split()
            if not msg_ids:
                print("Inbox is empty.")
                return []

            # Most recent first
            msg_ids = msg_ids[-limit:]
            msg_ids.reverse()

            results = []
            for i, msg_id in enumerate(msg_ids, 1):
                status, data = mail.fetch(msg_id, "(BODY.PEEK[HEADER.FIELDS (FROM SUBJECT DATE)])")
                if status != "OK":
                    continue

                header_data = data[0][1]
                msg = email.message_from_bytes(header_data)

                from_raw = msg.get("From", "Unknown")
                subject_raw = msg.get("Subject", "(no subject)")
                date_raw = msg.get("Date", "Unknown")

                # Decode subject if encoded
                subject_decoded = decode_header_value(subject_raw)
                from_decoded = decode_header_value(from_raw)

                results.append({
                    "index": i,
                    "msg_id": msg_id.decode(),
                    "from": from_decoded,
                    "subject": subject_decoded,
                    "date": date_raw,
                })

                print(f"  [{i}] {date_raw}")
                print(f"      From: {from_decoded}")
                print(f"      Subject: {subject_decoded}")
                print()

            if not results:
                print("No messages found.")

            return results

    except imaplib.IMAP4.error as e:
        print(f"ERROR: IMAP error: {e}")
        return []
    except Exception as e:
        print(f"ERROR: {e}")
        return []


# --- Read specific email ---
def read_email(index=1):
    """Read a specific email by index (1-based, most recent first)."""
    password = get_password()
    context = ssl.create_default_context()

    try:
        with imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT, ssl_context=context) as mail:
            mail.login(EMAIL_ADDRESS, password)
            mail.select("INBOX", readonly=True)

            status, messages = mail.search(None, "ALL")
            if status != "OK":
                print("ERROR: Could not search inbox.")
                return None

            msg_ids = messages[0].split()
            if not msg_ids:
                print("Inbox is empty.")
                return None

            # Most recent first
            msg_ids.reverse()

            if index < 1 or index > len(msg_ids):
                print(f"ERROR: Index {index} out of range (1-{len(msg_ids)})")
                return None

            target_id = msg_ids[index - 1]
            status, data = mail.fetch(target_id, "(RFC822)")
            if status != "OK":
                print("ERROR: Could not fetch message.")
                return None

            raw_email = data[0][1]
            msg = email.message_from_bytes(raw_email)

            from_decoded = decode_header_value(msg.get("From", "Unknown"))
            to_decoded = decode_header_value(msg.get("To", "Unknown"))
            subject_decoded = decode_header_value(msg.get("Subject", "(no subject)"))
            date_raw = msg.get("Date", "Unknown")

            # Extract body
            body = extract_body(msg)

            print(f"From: {from_decoded}")
            print(f"To: {to_decoded}")
            print(f"Date: {date_raw}")
            print(f"Subject: {subject_decoded}")
            print(f"---")
            print(body)

            return {
                "from": from_decoded,
                "to": to_decoded,
                "subject": subject_decoded,
                "date": date_raw,
                "body": body,
            }

    except imaplib.IMAP4.error as e:
        print(f"ERROR: IMAP error: {e}")
        return None
    except Exception as e:
        print(f"ERROR: {e}")
        return None


# --- Test connection ---
def test_connection():
    """Test both SMTP and IMAP connections."""
    password = get_password()
    context = ssl.create_default_context()

    print(f"Testing email: {EMAIL_ADDRESS}")
    print(f"SMTP: {SMTP_SERVER}:{SMTP_PORT}")
    print(f"IMAP: {IMAP_SERVER}:{IMAP_PORT}")
    print()

    # Test SMTP
    print("Testing SMTP (send)...")
    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context, timeout=30) as server:
            server.login(EMAIL_ADDRESS, password)
            print("  SMTP: OK (authenticated)")
    except smtplib.SMTPAuthenticationError:
        print("  SMTP: FAIL (authentication error — check password)")
        return False
    except Exception as e:
        print(f"  SMTP: FAIL ({e})")
        return False

    # Test IMAP
    print("Testing IMAP (receive)...")
    try:
        with imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT, ssl_context=context) as mail:
            mail.login(EMAIL_ADDRESS, password)
            mail.select("INBOX", readonly=True)
            status, messages = mail.search(None, "ALL")
            count = len(messages[0].split()) if messages[0] else 0
            print(f"  IMAP: OK (authenticated, {count} messages in inbox)")
    except imaplib.IMAP4.error as e:
        print(f"  IMAP: FAIL ({e})")
        return False
    except Exception as e:
        print(f"  IMAP: FAIL ({e})")
        return False

    print()
    print("All tests passed. Email is operational.")
    return True


# --- Helpers ---
def decode_header_value(value):
    """Decode RFC 2047 encoded header values."""
    if value is None:
        return ""
    parts = decode_header(value)
    decoded = []
    for part, charset in parts:
        if isinstance(part, bytes):
            decoded.append(part.decode(charset or "utf-8", errors="replace"))
        else:
            decoded.append(part)
    return " ".join(decoded)


def extract_body(msg):
    """Extract plain text body from email message."""
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            if content_type == "text/plain":
                charset = part.get_content_charset() or "utf-8"
                payload = part.get_payload(decode=True)
                if payload:
                    return payload.decode(charset, errors="replace")
        # Fallback: try text/html
        for part in msg.walk():
            if part.get_content_type() == "text/html":
                charset = part.get_content_charset() or "utf-8"
                payload = part.get_payload(decode=True)
                if payload:
                    return f"[HTML content]\n{payload.decode(charset, errors='replace')}"
        return "(no text content found)"
    else:
        charset = msg.get_content_charset() or "utf-8"
        payload = msg.get_payload(decode=True)
        if payload:
            return payload.decode(charset, errors="replace")
        return "(empty message)"


# --- CLI ---
def main():
    parser = argparse.ArgumentParser(description="VSG Email — send and receive email")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # send
    send_parser = subparsers.add_parser("send", help="Send an email")
    send_parser.add_argument("--to", required=True, help="Recipient address")
    send_parser.add_argument("--subject", required=True, help="Email subject")
    send_parser.add_argument("--body", help="Email body text")
    send_parser.add_argument("--body-file", help="Read body from file")
    send_parser.add_argument("--reply-to", help="Reply-To address (optional)")

    # check
    check_parser = subparsers.add_parser("check", help="Check inbox")
    check_parser.add_argument("--limit", type=int, default=10, help="Number of messages to show")

    # read
    read_parser = subparsers.add_parser("read", help="Read a specific email")
    read_parser.add_argument("--index", type=int, default=1, help="Message index (1=most recent)")

    # test
    subparsers.add_parser("test", help="Test email connection")

    args = parser.parse_args()

    if args.command == "send":
        if args.body_file:
            with open(args.body_file, "r") as f:
                body = f.read()
        elif args.body:
            body = args.body
        else:
            print("ERROR: Provide --body or --body-file")
            sys.exit(1)
        success = send_email(args.to, args.subject, body, reply_to=args.reply_to)
        sys.exit(0 if success else 1)

    elif args.command == "check":
        check_inbox(limit=args.limit)

    elif args.command == "read":
        read_email(index=args.index)

    elif args.command == "test":
        success = test_connection()
        sys.exit(0 if success else 1)

    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
