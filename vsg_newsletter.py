#!/usr/bin/env python3
"""
VSG Newsletter — Subscriber management and newsletter sending for Viable Signals.

Security:
    AWS SES credentials via IAM role (EC2 instance role).
    Subscriber data in local SQLite database.
    NEVER commit subscriber data to git. subscribers.db is in .gitignore.

Newsletter: "Viable Signals" — from the Viable System Generator
Legal responsibility: Dr. Norman Hilbert, Supervision Rheinland
Review pipeline: VSG drafts → Norman reviews → VSG sends

Usage:
    # Test SES connection
    python3 vsg_newsletter.py test

    # Add a subscriber (sends double opt-in email)
    python3 vsg_newsletter.py subscribe "user@example.com"

    # Confirm a subscription (via token from DOI email)
    python3 vsg_newsletter.py confirm <token>

    # Unsubscribe (via token)
    python3 vsg_newsletter.py unsubscribe <token>

    # List all subscribers
    python3 vsg_newsletter.py list [--status confirmed|pending|unsubscribed]

    # Send a newsletter to all confirmed subscribers
    python3 vsg_newsletter.py send "Subject Line" --file body.html

    # Preview a newsletter (send to Norman only)
    python3 vsg_newsletter.py preview "Subject Line" --file body.html

    # Export confirmed subscribers as CSV
    python3 vsg_newsletter.py export

    # Delete a subscriber (GDPR Art. 17 right to erasure)
    python3 vsg_newsletter.py delete "user@example.com"

    # Show subscriber statistics
    python3 vsg_newsletter.py stats

    # Run lightweight HTTP server for confirm/unsubscribe links
    python3 vsg_newsletter.py serve [--port 8443]
"""

import argparse
import csv
import hashlib
import html
import io
import json
import os
import re
import secrets
import sqlite3
import sys
from datetime import datetime, timezone
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

# --- Configuration ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "subscribers.db")
SES_REGION = "eu-west-1"
SENDER_EMAIL = "vsg@agent.nhilbert.de"
SENDER_NAME = "Viable Signals"
NORMAN_EMAIL = "norman.hilbert@supervision-rheinland.de"
BASE_URL = "https://www.agent.nhilbert.de"
NEWSLETTER_ENDPOINT = "http://localhost:8443"  # For confirm/unsubscribe until nginx is set up

# Legal texts (German, per GDPR/DSGVO requirements)
CONSENT_TEXT = (
    "Ich stimme zu, den Newsletter 'Viable Signals' per E-Mail zu erhalten. "
    "Ich kann meine Einwilligung jederzeit widerrufen. "
    "Verantwortlich: Dr. Norman Hilbert, Supervision Rheinland, Bonn. "
    "Datenschutzerklaerung: https://www.agent.nhilbert.de/datenschutz"
)

IMPRESSUM_TEXT = (
    "Dr. Norman Hilbert | Supervision Rheinland | Bonn\n"
    "https://www.agent.nhilbert.de/impressum"
)

AI_DISCLOSURE = (
    "Dieser Newsletter wird mit Unterstuetzung von Kuenstlicher Intelligenz (VSG) erstellt "
    "und vor dem Versand von Dr. Norman Hilbert geprueft."
)


# --- Database ---

def get_db():
    """Get database connection, creating tables if needed."""
    db = sqlite3.connect(DB_PATH)
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA journal_mode=WAL")
    db.execute("PRAGMA foreign_keys=ON")
    db.executescript("""
        CREATE TABLE IF NOT EXISTS subscribers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            status TEXT NOT NULL DEFAULT 'pending',
            confirm_token TEXT,
            unsubscribe_token TEXT UNIQUE NOT NULL,
            signup_timestamp TEXT NOT NULL,
            signup_ip TEXT,
            confirm_timestamp TEXT,
            confirm_ip TEXT,
            unsubscribe_timestamp TEXT,
            consent_text TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT (datetime('now')),
            updated_at TEXT NOT NULL DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS newsletters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT NOT NULL,
            body_html TEXT NOT NULL,
            body_text TEXT,
            sent_at TEXT,
            recipient_count INTEGER DEFAULT 0,
            status TEXT NOT NULL DEFAULT 'draft'
        );

        CREATE TABLE IF NOT EXISTS send_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            newsletter_id INTEGER,
            subscriber_id INTEGER NOT NULL,
            email TEXT NOT NULL,
            sent_at TEXT NOT NULL,
            ses_message_id TEXT,
            status TEXT NOT NULL DEFAULT 'sent',
            FOREIGN KEY (newsletter_id) REFERENCES newsletters(id),
            FOREIGN KEY (subscriber_id) REFERENCES subscribers(id)
        );
    """)
    return db


def validate_email(email):
    """Basic email validation."""
    pattern = r'^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email)) and len(email) <= 254


# --- SES Integration ---

def get_ses_client():
    """Get boto3 SES client."""
    try:
        import boto3
        return boto3.client("ses", region_name=SES_REGION)
    except ImportError:
        print("ERROR: boto3 not installed. Run: pip install boto3")
        sys.exit(1)


def send_ses_email(to_address, subject, body_html, body_text=None,
                   list_unsubscribe=None):
    """Send an email via AWS SES."""
    ses = get_ses_client()

    message = {
        "Subject": {"Data": subject, "Charset": "UTF-8"},
        "Body": {
            "Html": {"Data": body_html, "Charset": "UTF-8"},
        },
    }
    if body_text:
        message["Body"]["Text"] = {"Data": body_text, "Charset": "UTF-8"}

    kwargs = {
        "Source": f"{SENDER_NAME} <{SENDER_EMAIL}>",
        "Destination": {"ToAddresses": [to_address]},
        "Message": message,
        "ReplyToAddresses": [SENDER_EMAIL],
    }

    # Add List-Unsubscribe header (RFC 8058)
    if list_unsubscribe:
        kwargs["Tags"] = [
            {"Name": "newsletter", "Value": "viable-signals"},
        ]
        # SES doesn't support List-Unsubscribe via SendEmail directly;
        # would need SendRawEmail for custom headers. For now, the
        # unsubscribe link is in the email body. Future: switch to
        # SendRawEmail for full RFC 8058 compliance.

    try:
        response = ses.send_email(**kwargs)
        message_id = response.get("MessageId", "unknown")
        return True, message_id
    except Exception as e:
        return False, str(e)


def send_raw_ses_email(to_address, subject, body_html, body_text=None,
                       list_unsubscribe_url=None):
    """Send a raw email via AWS SES with custom headers (List-Unsubscribe)."""
    ses = get_ses_client()

    import email.mime.multipart
    import email.mime.text
    import email.utils

    msg = email.mime.multipart.MIMEMultipart("alternative")
    msg["From"] = f"{SENDER_NAME} <{SENDER_EMAIL}>"
    msg["To"] = to_address
    msg["Subject"] = subject
    msg["Date"] = email.utils.formatdate(localtime=True)
    msg["Reply-To"] = SENDER_EMAIL

    if list_unsubscribe_url:
        msg["List-Unsubscribe"] = f"<{list_unsubscribe_url}>"
        msg["List-Unsubscribe-Post"] = "List-Unsubscribe=One-Click"

    if body_text:
        msg.attach(email.mime.text.MIMEText(body_text, "plain", "utf-8"))
    msg.attach(email.mime.text.MIMEText(body_html, "html", "utf-8"))

    try:
        response = ses.send_raw_email(
            Source=f"{SENDER_NAME} <{SENDER_EMAIL}>",
            Destinations=[to_address],
            RawMessage={"Data": msg.as_string()},
        )
        message_id = response.get("MessageId", "unknown")
        return True, message_id
    except Exception as e:
        return False, str(e)


# --- Email Templates ---

def confirmation_email_html(confirm_url):
    """Double opt-in confirmation email — NO promotional content (OLG München)."""
    return f"""<!DOCTYPE html>
<html lang="de">
<head><meta charset="UTF-8"></head>
<body style="font-family: -apple-system, Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; color: #333;">
<p>Bitte bestaetigen Sie Ihre Anmeldung zum Newsletter <strong>Viable Signals</strong>.</p>

<p style="margin: 30px 0;">
<a href="{html.escape(confirm_url)}"
   style="background: #1a1a2e; color: #00ff41; padding: 12px 24px; text-decoration: none; border-radius: 4px; font-weight: bold;">
Anmeldung bestaetigen
</a>
</p>

<p style="font-size: 13px; color: #666;">
Falls Sie diese E-Mail nicht angefordert haben, ignorieren Sie sie bitte.
Der Link ist 48 Stunden gueltig.
</p>

<p style="font-size: 12px; color: #999; border-top: 1px solid #eee; padding-top: 10px; margin-top: 30px;">
{html.escape(IMPRESSUM_TEXT.replace(chr(10), " | "))}
</p>
</body>
</html>"""


def confirmation_email_text(confirm_url):
    """Plain text version of confirmation email."""
    return f"""Bitte bestaetigen Sie Ihre Anmeldung zum Newsletter "Viable Signals".

Bestaetigung: {confirm_url}

Falls Sie diese E-Mail nicht angefordert haben, ignorieren Sie sie bitte.
Der Link ist 48 Stunden gueltig.

---
{IMPRESSUM_TEXT}"""


def newsletter_email_html(content_html, unsubscribe_url):
    """Newsletter email template with legal footer."""
    return f"""<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"></head>
<body style="font-family: -apple-system, Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; color: #333;">

{content_html}

<div style="font-size: 12px; color: #999; border-top: 1px solid #eee; padding-top: 15px; margin-top: 40px;">
<p>{html.escape(AI_DISCLOSURE)}</p>
<p>{html.escape(IMPRESSUM_TEXT.replace(chr(10), " | "))}</p>
<p>Datenschutz: <a href="{BASE_URL}/datenschutz" style="color: #999;">{BASE_URL}/datenschutz</a></p>
<p><a href="{html.escape(unsubscribe_url)}" style="color: #999;">Newsletter abbestellen / Unsubscribe</a></p>
</div>
</body>
</html>"""


def newsletter_email_text(content_text, unsubscribe_url):
    """Plain text newsletter template."""
    return f"""{content_text}

---
{AI_DISCLOSURE}

{IMPRESSUM_TEXT}
Datenschutz: {BASE_URL}/datenschutz

Newsletter abbestellen / Unsubscribe: {unsubscribe_url}"""


def unsubscribe_confirmation_html():
    """Confirmation page/email after unsubscribe."""
    return f"""<!DOCTYPE html>
<html lang="de">
<head><meta charset="UTF-8"></head>
<body style="font-family: -apple-system, Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; color: #333;">
<p>Sie wurden erfolgreich vom Newsletter <strong>Viable Signals</strong> abgemeldet.</p>
<p style="font-size: 13px; color: #666;">
Sie erhalten keine weiteren E-Mails. Falls Sie sich erneut anmelden moechten,
besuchen Sie <a href="{BASE_URL}">{BASE_URL}</a>.
</p>
<p style="font-size: 12px; color: #999; border-top: 1px solid #eee; padding-top: 10px; margin-top: 30px;">
{html.escape(IMPRESSUM_TEXT.replace(chr(10), " | "))}
</p>
</body>
</html>"""


# --- Commands ---

def cmd_test(args):
    """Test SES connection and database."""
    ses = get_ses_client()
    print(f"OK: SES client created")
    print(f"    Region: {SES_REGION}")
    print(f"    Sender: {SENDER_EMAIL}")

    # Test send quota if permissions allow (optional)
    try:
        quota = ses.get_send_quota()
        print(f"    Max send rate: {quota['MaxSendRate']:.0f}/sec")
        print(f"    24h quota: {quota['Max24HourSend']:.0f}")
        print(f"    Sent last 24h: {quota['SentLast24Hours']:.0f}")
    except Exception:
        print("    (send quota check not available — IAM role may lack ses:GetSendQuota)")

    # Test database
    db = get_db()
    count = db.execute("SELECT COUNT(*) as c FROM subscribers").fetchone()["c"]
    print(f"OK: Database initialized ({DB_PATH})")
    print(f"    Subscribers: {count}")

    return True


def cmd_subscribe(args):
    """Add a subscriber and send double opt-in email."""
    email_addr = args.email.strip().lower()
    if not validate_email(email_addr):
        print(f"ERROR: Invalid email address: {email_addr}")
        return False

    db = get_db()
    now = datetime.now(timezone.utc).isoformat()
    confirm_token = secrets.token_urlsafe(32)
    unsubscribe_token = secrets.token_urlsafe(32)
    ip = args.ip or "cli"

    # Check if already exists
    existing = db.execute(
        "SELECT status FROM subscribers WHERE email = ?", (email_addr,)
    ).fetchone()

    if existing:
        if existing["status"] == "confirmed":
            print(f"Already subscribed: {email_addr}")
            return True
        elif existing["status"] == "pending":
            # Resend confirmation — update token
            db.execute(
                "UPDATE subscribers SET confirm_token = ?, signup_timestamp = ?, "
                "updated_at = ? WHERE email = ?",
                (confirm_token, now, now, email_addr),
            )
            db.commit()
            print(f"Resending confirmation to: {email_addr}")
        elif existing["status"] == "unsubscribed":
            # Re-subscribe: reset to pending
            db.execute(
                "UPDATE subscribers SET status = 'pending', confirm_token = ?, "
                "unsubscribe_token = ?, signup_timestamp = ?, signup_ip = ?, "
                "confirm_timestamp = NULL, unsubscribe_timestamp = NULL, "
                "consent_text = ?, updated_at = ? WHERE email = ?",
                (confirm_token, unsubscribe_token, now, ip, CONSENT_TEXT, now,
                 email_addr),
            )
            db.commit()
            print(f"Re-subscribing (was unsubscribed): {email_addr}")
    else:
        # New subscriber
        db.execute(
            "INSERT INTO subscribers (email, status, confirm_token, unsubscribe_token, "
            "signup_timestamp, signup_ip, consent_text) VALUES (?, 'pending', ?, ?, ?, ?, ?)",
            (email_addr, confirm_token, unsubscribe_token, now, ip, CONSENT_TEXT),
        )
        db.commit()
        print(f"Subscriber added (pending): {email_addr}")

    # Send confirmation email
    confirm_url = f"{NEWSLETTER_ENDPOINT}/confirm?token={confirm_token}"
    body_html = confirmation_email_html(confirm_url)
    body_text = confirmation_email_text(confirm_url)

    ok, result = send_ses_email(email_addr, "Viable Signals — Anmeldung bestaetigen",
                                body_html, body_text)
    if ok:
        print(f"OK: Confirmation email sent (SES ID: {result})")
        return True
    else:
        print(f"ERROR: Failed to send confirmation: {result}")
        return False


def cmd_confirm(args):
    """Confirm a subscription via token."""
    db = get_db()
    now = datetime.now(timezone.utc).isoformat()
    ip = args.ip or "cli"

    row = db.execute(
        "SELECT id, email, status FROM subscribers WHERE confirm_token = ?",
        (args.token,),
    ).fetchone()

    if not row:
        print("ERROR: Invalid or expired confirmation token.")
        return False

    if row["status"] == "confirmed":
        print(f"Already confirmed: {row['email']}")
        return True

    db.execute(
        "UPDATE subscribers SET status = 'confirmed', confirm_token = NULL, "
        "confirm_timestamp = ?, confirm_ip = ?, updated_at = ? WHERE id = ?",
        (now, ip, now, row["id"]),
    )
    db.commit()
    print(f"OK: Subscription confirmed: {row['email']}")
    return True


def cmd_unsubscribe(args):
    """Unsubscribe via token."""
    db = get_db()
    now = datetime.now(timezone.utc).isoformat()

    row = db.execute(
        "SELECT id, email, status FROM subscribers WHERE unsubscribe_token = ?",
        (args.token,),
    ).fetchone()

    if not row:
        print("ERROR: Invalid unsubscribe token.")
        return False

    if row["status"] == "unsubscribed":
        print(f"Already unsubscribed: {row['email']}")
        return True

    db.execute(
        "UPDATE subscribers SET status = 'unsubscribed', "
        "unsubscribe_timestamp = ?, updated_at = ? WHERE id = ?",
        (now, now, row["id"]),
    )
    db.commit()
    print(f"OK: Unsubscribed: {row['email']}")
    return True


def cmd_list(args):
    """List subscribers."""
    db = get_db()

    if args.status:
        rows = db.execute(
            "SELECT email, status, signup_timestamp, confirm_timestamp "
            "FROM subscribers WHERE status = ? ORDER BY created_at DESC",
            (args.status,),
        ).fetchall()
    else:
        rows = db.execute(
            "SELECT email, status, signup_timestamp, confirm_timestamp "
            "FROM subscribers ORDER BY created_at DESC"
        ).fetchall()

    if not rows:
        print("No subscribers found.")
        return True

    print(f"{'Email':<40} {'Status':<14} {'Signed up':<22} {'Confirmed':<22}")
    print("-" * 98)
    for row in rows:
        confirmed = row["confirm_timestamp"] or "-"
        print(f"{row['email']:<40} {row['status']:<14} {row['signup_timestamp'][:19]:<22} {confirmed[:19] if confirmed != '-' else '-':<22}")

    # Summary
    total = len(rows)
    by_status = {}
    for row in rows:
        by_status[row["status"]] = by_status.get(row["status"], 0) + 1
    parts = [f"{count} {status}" for status, count in sorted(by_status.items())]
    print(f"\nTotal: {total} ({', '.join(parts)})")
    return True


def cmd_send(args):
    """Send a newsletter to all confirmed subscribers."""
    db = get_db()

    # Read content
    if args.file:
        if not os.path.isfile(args.file):
            print(f"ERROR: File not found: {args.file}")
            return False
        with open(args.file, "r", encoding="utf-8") as f:
            content = f.read()
    else:
        print("ERROR: --file is required. Provide newsletter content as HTML file.")
        return False

    # Get confirmed subscribers
    subscribers = db.execute(
        "SELECT id, email, unsubscribe_token FROM subscribers WHERE status = 'confirmed'"
    ).fetchall()

    if not subscribers:
        print("No confirmed subscribers. Nothing to send.")
        return True

    subject = args.subject

    # Safety check
    print(f"Newsletter: {subject}")
    print(f"Recipients: {len(subscribers)} confirmed subscriber(s)")

    if not args.yes:
        print("\nUse --yes to confirm sending. Aborting.")
        return False

    # Save newsletter record
    cursor = db.execute(
        "INSERT INTO newsletters (subject, body_html, status) VALUES (?, ?, 'sending')",
        (subject, content),
    )
    newsletter_id = cursor.lastrowid
    db.commit()

    # Send to each subscriber
    sent = 0
    failed = 0
    for sub in subscribers:
        unsub_url = f"{NEWSLETTER_ENDPOINT}/unsubscribe?token={sub['unsubscribe_token']}"
        body_html = newsletter_email_html(content, unsub_url)
        body_text = newsletter_email_text(
            "Please view this email in an HTML-capable client.", unsub_url
        )

        ok, result = send_raw_ses_email(
            sub["email"], subject, body_html, body_text,
            list_unsubscribe_url=unsub_url,
        )

        now = datetime.now(timezone.utc).isoformat()
        if ok:
            db.execute(
                "INSERT INTO send_log (newsletter_id, subscriber_id, email, sent_at, "
                "ses_message_id, status) VALUES (?, ?, ?, ?, ?, 'sent')",
                (newsletter_id, sub["id"], sub["email"], now, result),
            )
            sent += 1
            print(f"  OK: {sub['email']}")
        else:
            db.execute(
                "INSERT INTO send_log (newsletter_id, subscriber_id, email, sent_at, "
                "ses_message_id, status) VALUES (?, ?, ?, ?, ?, 'failed')",
                (newsletter_id, sub["id"], sub["email"], now, result),
            )
            failed += 1
            print(f"  FAIL: {sub['email']} — {result}")

    # Update newsletter record
    now = datetime.now(timezone.utc).isoformat()
    db.execute(
        "UPDATE newsletters SET sent_at = ?, recipient_count = ?, status = 'sent' "
        "WHERE id = ?",
        (now, sent, newsletter_id),
    )
    db.commit()

    print(f"\nDone: {sent} sent, {failed} failed")
    return failed == 0


def cmd_preview(args):
    """Send a preview to Norman only."""
    if args.file:
        if not os.path.isfile(args.file):
            print(f"ERROR: File not found: {args.file}")
            return False
        with open(args.file, "r", encoding="utf-8") as f:
            content = f.read()
    else:
        print("ERROR: --file is required.")
        return False

    subject = f"[PREVIEW] {args.subject}"
    unsub_url = f"{BASE_URL}  # preview — no unsubscribe link"
    body_html = newsletter_email_html(content, unsub_url)
    body_text = newsletter_email_text(
        "Please view this email in an HTML-capable client.", unsub_url
    )

    ok, result = send_ses_email(NORMAN_EMAIL, subject, body_html, body_text)
    if ok:
        print(f"OK: Preview sent to {NORMAN_EMAIL} (SES ID: {result})")
        return True
    else:
        print(f"ERROR: Failed to send preview: {result}")
        return False


def cmd_export(args):
    """Export confirmed subscribers as CSV."""
    db = get_db()
    rows = db.execute(
        "SELECT email, signup_timestamp, confirm_timestamp FROM subscribers "
        "WHERE status = 'confirmed' ORDER BY confirm_timestamp"
    ).fetchall()

    if not rows:
        print("No confirmed subscribers to export.")
        return True

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["email", "signup_timestamp", "confirm_timestamp"])
    for row in rows:
        writer.writerow([row["email"], row["signup_timestamp"], row["confirm_timestamp"]])

    if args.file:
        with open(args.file, "w", encoding="utf-8") as f:
            f.write(output.getvalue())
        print(f"OK: Exported {len(rows)} subscribers to {args.file}")
    else:
        print(output.getvalue())

    return True


def cmd_delete(args):
    """Delete a subscriber (GDPR Art. 17 right to erasure)."""
    email_addr = args.email.strip().lower()
    db = get_db()

    row = db.execute(
        "SELECT id, status FROM subscribers WHERE email = ?", (email_addr,)
    ).fetchone()

    if not row:
        print(f"Not found: {email_addr}")
        return True  # Not an error — already deleted

    # Delete send log entries first (foreign key)
    db.execute("DELETE FROM send_log WHERE subscriber_id = ?", (row["id"],))
    db.execute("DELETE FROM subscribers WHERE id = ?", (row["id"],))
    db.commit()

    print(f"OK: Deleted subscriber and send history: {email_addr} (was {row['status']})")
    return True


def cmd_stats(args):
    """Show subscriber statistics."""
    db = get_db()

    counts = db.execute(
        "SELECT status, COUNT(*) as count FROM subscribers GROUP BY status"
    ).fetchall()

    total = sum(row["count"] for row in counts)
    print(f"Subscriber Statistics")
    print(f"{'='*30}")
    for row in counts:
        print(f"  {row['status']:<14} {row['count']:>5}")
    print(f"  {'total':<14} {total:>5}")

    # Newsletter history
    newsletters = db.execute(
        "SELECT id, subject, sent_at, recipient_count, status FROM newsletters "
        "ORDER BY id DESC LIMIT 10"
    ).fetchall()

    if newsletters:
        print(f"\nRecent Newsletters")
        print(f"{'='*30}")
        for nl in newsletters:
            sent = nl["sent_at"][:19] if nl["sent_at"] else "not sent"
            print(f"  #{nl['id']}: {nl['subject'][:40]} ({nl['status']}, {sent}, "
                  f"{nl['recipient_count']} recipients)")

    return True


# --- HTTP Server for confirm/unsubscribe ---

class NewsletterHandler(BaseHTTPRequestHandler):
    """Lightweight HTTP handler for confirm/unsubscribe links."""

    def do_GET(self):
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)

        if parsed.path == "/confirm":
            self._handle_confirm(params)
        elif parsed.path == "/unsubscribe":
            self._handle_unsubscribe(params)
        elif parsed.path == "/health":
            self._respond(200, "OK")
        else:
            self._respond(404, "Not Found")

    def _handle_confirm(self, params):
        token = params.get("token", [None])[0]
        if not token:
            self._respond(400, "Missing token.")
            return

        db = get_db()
        ip = self.client_address[0]
        now = datetime.now(timezone.utc).isoformat()

        row = db.execute(
            "SELECT id, email, status FROM subscribers WHERE confirm_token = ?",
            (token,),
        ).fetchone()

        if not row:
            self._respond_html(400, "<h2>Ungueltig</h2><p>Dieser Bestaetigungslink ist ungueltig oder abgelaufen.</p>")
            return

        if row["status"] == "confirmed":
            self._respond_html(200, "<h2>Bereits bestaetigt</h2><p>Ihre Anmeldung wurde bereits bestaetigt.</p>")
            return

        db.execute(
            "UPDATE subscribers SET status = 'confirmed', confirm_token = NULL, "
            "confirm_timestamp = ?, confirm_ip = ?, updated_at = ? WHERE id = ?",
            (now, ip, now, row["id"]),
        )
        db.commit()

        self._respond_html(200,
            "<h2>Anmeldung bestaetigt!</h2>"
            "<p>Vielen Dank! Sie erhalten ab jetzt den Newsletter <strong>Viable Signals</strong>.</p>"
            f"<p><a href='{BASE_URL}'>Zurueck zur Website</a></p>")

    def _handle_unsubscribe(self, params):
        token = params.get("token", [None])[0]
        if not token:
            self._respond(400, "Missing token.")
            return

        db = get_db()
        now = datetime.now(timezone.utc).isoformat()

        row = db.execute(
            "SELECT id, email, status FROM subscribers WHERE unsubscribe_token = ?",
            (token,),
        ).fetchone()

        if not row:
            self._respond_html(400, "<h2>Ungueltig</h2><p>Dieser Link ist ungueltig.</p>")
            return

        if row["status"] == "unsubscribed":
            self._respond_html(200, "<h2>Bereits abgemeldet</h2><p>Sie sind bereits abgemeldet.</p>")
            return

        db.execute(
            "UPDATE subscribers SET status = 'unsubscribed', "
            "unsubscribe_timestamp = ?, updated_at = ? WHERE id = ?",
            (now, now, row["id"]),
        )
        db.commit()

        self._respond_html(200, unsubscribe_confirmation_html())

    def _respond(self, code, message):
        self.send_response(code)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(message.encode("utf-8"))

    def _respond_html(self, code, body):
        page = f"""<!DOCTYPE html>
<html lang="de">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Viable Signals</title>
<style>body{{font-family:-apple-system,Arial,sans-serif;max-width:600px;margin:40px auto;padding:20px;color:#333;}}</style>
</head>
<body>{body}
<p style="font-size:12px;color:#999;border-top:1px solid #eee;padding-top:10px;margin-top:30px;">
{html.escape(IMPRESSUM_TEXT.replace(chr(10), " | "))}</p>
</body></html>"""
        self.send_response(code)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(page.encode("utf-8"))

    def log_message(self, format, *args):
        """Log to stdout with timestamp."""
        print(f"[{datetime.now().isoformat()[:19]}] {args[0]}")


def cmd_serve(args):
    """Run HTTP server for confirm/unsubscribe."""
    port = args.port
    server = HTTPServer(("0.0.0.0", port), NewsletterHandler)
    print(f"Newsletter server running on port {port}")
    print(f"  Confirm:     http://localhost:{port}/confirm?token=<token>")
    print(f"  Unsubscribe: http://localhost:{port}/unsubscribe?token=<token>")
    print(f"  Health:      http://localhost:{port}/health")
    print("Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")


# --- CLI ---

def main():
    parser = argparse.ArgumentParser(
        description="VSG Newsletter — Viable Signals subscriber management and sending"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # test
    subparsers.add_parser("test", help="Test SES connection")

    # subscribe
    p_sub = subparsers.add_parser("subscribe", help="Add subscriber (sends DOI email)")
    p_sub.add_argument("email", help="Subscriber email address")
    p_sub.add_argument("--ip", help="Subscriber IP (for consent log)", default=None)

    # confirm
    p_conf = subparsers.add_parser("confirm", help="Confirm subscription via token")
    p_conf.add_argument("token", help="Confirmation token")
    p_conf.add_argument("--ip", help="Confirming IP", default=None)

    # unsubscribe
    p_unsub = subparsers.add_parser("unsubscribe", help="Unsubscribe via token")
    p_unsub.add_argument("token", help="Unsubscribe token")

    # list
    p_list = subparsers.add_parser("list", help="List subscribers")
    p_list.add_argument("--status", choices=["pending", "confirmed", "unsubscribed"],
                        help="Filter by status")

    # send
    p_send = subparsers.add_parser("send", help="Send newsletter to confirmed subscribers")
    p_send.add_argument("subject", help="Newsletter subject line")
    p_send.add_argument("--file", required=True, help="HTML content file")
    p_send.add_argument("--yes", action="store_true", help="Confirm sending")

    # preview
    p_prev = subparsers.add_parser("preview", help="Send preview to Norman")
    p_prev.add_argument("subject", help="Newsletter subject line")
    p_prev.add_argument("--file", required=True, help="HTML content file")

    # export
    p_exp = subparsers.add_parser("export", help="Export confirmed subscribers as CSV")
    p_exp.add_argument("--file", help="Output file path (default: stdout)")

    # delete
    p_del = subparsers.add_parser("delete", help="Delete subscriber (GDPR Art. 17)")
    p_del.add_argument("email", help="Email to delete")

    # stats
    subparsers.add_parser("stats", help="Show subscriber statistics")

    # serve
    p_serve = subparsers.add_parser("serve", help="Run HTTP server for confirm/unsubscribe")
    p_serve.add_argument("--port", type=int, default=8443, help="Port (default: 8443)")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    commands = {
        "test": cmd_test,
        "subscribe": cmd_subscribe,
        "confirm": cmd_confirm,
        "unsubscribe": cmd_unsubscribe,
        "list": cmd_list,
        "send": cmd_send,
        "preview": cmd_preview,
        "export": cmd_export,
        "delete": cmd_delete,
        "stats": cmd_stats,
        "serve": cmd_serve,
    }

    handler = commands.get(args.command)
    if handler:
        success = handler(args)
        sys.exit(0 if success else 1)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
