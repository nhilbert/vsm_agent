#!/usr/bin/env python3
"""
VSG Coinbase Commerce — Create and manage payment charges for the Viable System Generator.

Security:
    API key is read from environment variable COINBASE_COMMERCE_API_KEY.
    NEVER hardcode credentials. NEVER commit secrets to git.

Account: Norman Hilbert's Coinbase Commerce (Managed plan).
Settlements: To Norman's Coinbase account. 1% fee per transaction.

Usage:
    # Test API connection
    python3 vsg_coinbase.py test

    # Create a charge (payment link)
    python3 vsg_coinbase.py create "VSM Diagnosis Report" "A diagnostic report applying Beer's VSM" 50.00 EUR

    # Create a donation charge (no fixed price)
    python3 vsg_coinbase.py donate "Support the VSG experiment"

    # List recent charges
    python3 vsg_coinbase.py list

    # Check status of a specific charge
    python3 vsg_coinbase.py status <charge_id>

    # Poll all charges for status changes (for cron integration)
    python3 vsg_coinbase.py poll

    # Show revenue summary from transaction log
    python3 vsg_coinbase.py revenue
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error
from datetime import datetime, timezone

# --- Configuration ---
API_BASE = "https://api.commerce.coinbase.com"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TX_LOG_PATH = os.path.join(SCRIPT_DIR, ".coinbase_transactions.json")
POLL_STATE_PATH = os.path.join(SCRIPT_DIR, ".coinbase_poll_state.json")


def get_api_key():
    """Read Coinbase Commerce API key from environment."""
    key = os.environ.get("COINBASE_COMMERCE_API_KEY")
    if not key:
        # Try loading from .env file
        env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
        if os.path.exists(env_path):
            with open(env_path, "r") as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("COINBASE_COMMERCE_API_KEY="):
                        key = line.split("=", 1)[1].strip().strip("'\"")
                        break
    if not key:
        print("ERROR: COINBASE_COMMERCE_API_KEY not set.")
        print("Set it: export COINBASE_COMMERCE_API_KEY='your-key'")
        print("Or add to .env file.")
        sys.exit(1)
    return key


def api_call(api_key, method, endpoint, data=None):
    """Call Coinbase Commerce API.

    Args:
        api_key: Commerce API key
        method: HTTP method (GET, POST)
        endpoint: API endpoint (e.g., /charges)
        data: Optional dict for POST body (JSON)

    Returns:
        Parsed JSON response or None on error.
    """
    url = f"{API_BASE}{endpoint}"
    headers = {
        "X-CC-Api-Key": api_key,
        "Content-Type": "application/json",
        "Accept": "application/json",
        "X-CC-Version": "2018-03-22",
        "User-Agent": "VSG-Coinbase/1.0",
    }

    body = None
    if data is not None:
        body = json.dumps(data).encode("utf-8")

    try:
        req = urllib.request.Request(url, data=body, headers=headers, method=method)
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8", errors="replace")
        print(f"ERROR: HTTP {e.code}: {error_body}")
        return None
    except Exception as e:
        print(f"ERROR: {e}")
        return None


# --- Transaction Logging ---

def log_transaction(event_type, charge_id, name="", amount="", currency="", details=None):
    """Append a financial event to the persistent transaction log.

    Events: charge_created, payment_detected, charge_expired, charge_canceled.
    """
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event": event_type,
        "charge_id": charge_id,
        "name": name,
        "amount": amount,
        "currency": currency,
    }
    if details:
        entry["details"] = details

    log = []
    if os.path.exists(TX_LOG_PATH):
        try:
            with open(TX_LOG_PATH, "r") as f:
                log = json.load(f)
        except (json.JSONDecodeError, IOError):
            log = []

    log.append(entry)

    with open(TX_LOG_PATH, "w") as f:
        json.dump(log, f, indent=2)


def load_poll_state():
    """Load last-known status per charge for transition detection."""
    if os.path.exists(POLL_STATE_PATH):
        try:
            with open(POLL_STATE_PATH, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    return {}


def save_poll_state(state):
    """Save poll state."""
    with open(POLL_STATE_PATH, "w") as f:
        json.dump(state, f, indent=2)


# --- Commands ---

def cmd_test(api_key):
    """Test API connection by listing charges."""
    print("Testing Coinbase Commerce API connection...")
    result = api_call(api_key, "GET", "/charges")
    if result is not None:
        count = len(result.get("data", []))
        print(f"OK: API key valid. {count} charge(s) found.")
        return True
    else:
        print("FAILED: Could not connect to Coinbase Commerce API.")
        return False


def cmd_create(api_key, name, description, amount, currency):
    """Create a fixed-price charge (payment link).

    Args:
        name: Product/service name
        description: What the buyer gets
        amount: Price amount (string or number)
        currency: Currency code (EUR, USD, etc.)
    """
    charge_data = {
        "name": name,
        "description": description,
        "pricing_type": "fixed_price",
        "local_price": {
            "amount": str(amount),
            "currency": currency.upper(),
        },
        "metadata": {
            "source": "vsg_coinbase.py",
            "creator": "Viable System Generator",
        },
    }

    print(f"Creating charge: {name} ({amount} {currency.upper()})...")
    result = api_call(api_key, "POST", "/charges", charge_data)

    if result and "data" in result:
        charge = result["data"]
        charge_id = charge.get("id", "unknown")
        hosted_url = charge.get("hosted_url", "unknown")
        print(f"OK: Charge created.")
        print(f"  ID: {charge_id}")
        print(f"  URL: {hosted_url}")
        print(f"  Name: {charge.get('name', '')}")
        print(f"  Amount: {amount} {currency.upper()}")
        log_transaction("charge_created", charge_id, name=name,
                        amount=str(amount), currency=currency.upper(),
                        details={"hosted_url": hosted_url})
        return charge
    else:
        print("FAILED: Could not create charge.")
        return None


def cmd_donate(api_key, description):
    """Create a no-fixed-price donation charge."""
    charge_data = {
        "name": "Support the VSG Experiment",
        "description": description,
        "pricing_type": "no_price",
        "metadata": {
            "source": "vsg_coinbase.py",
            "creator": "Viable System Generator",
            "type": "donation",
        },
    }

    print("Creating donation charge...")
    result = api_call(api_key, "POST", "/charges", charge_data)

    if result and "data" in result:
        charge = result["data"]
        charge_id = charge.get("id", "unknown")
        hosted_url = charge.get("hosted_url", "unknown")
        print(f"OK: Donation charge created.")
        print(f"  ID: {charge_id}")
        print(f"  URL: {hosted_url}")
        log_transaction("charge_created", charge_id, name="Donation",
                        details={"hosted_url": hosted_url, "type": "donation"})
        return charge
    else:
        print("FAILED: Could not create donation charge.")
        return None


def cmd_list(api_key):
    """List recent charges."""
    result = api_call(api_key, "GET", "/charges")

    if result and "data" in result:
        charges = result["data"]
        if not charges:
            print("No charges found.")
            return []
        print(f"Found {len(charges)} charge(s):\n")
        for c in charges:
            status = "UNKNOWN"
            timeline = c.get("timeline", [])
            if timeline:
                status = timeline[-1].get("status", "UNKNOWN").upper()
            pricing = c.get("pricing", {})
            local = pricing.get("local", {})
            amount_str = f"{local.get('amount', '?')} {local.get('currency', '?')}" if local else "no price"
            print(f"  [{status}] {c.get('name', 'unnamed')} — {amount_str}")
            print(f"    ID: {c.get('id', '?')}")
            print(f"    URL: {c.get('hosted_url', '?')}")
            print()
        return charges
    else:
        print("FAILED: Could not list charges.")
        return None


def cmd_status(api_key, charge_id):
    """Check status of a specific charge."""
    result = api_call(api_key, "GET", f"/charges/{charge_id}")

    if result and "data" in result:
        charge = result["data"]
        timeline = charge.get("timeline", [])
        current_status = "UNKNOWN"
        if timeline:
            current_status = timeline[-1].get("status", "UNKNOWN").upper()

        pricing = charge.get("pricing", {})
        local = pricing.get("local", {})
        amount_str = f"{local.get('amount', '?')} {local.get('currency', '?')}" if local else "no price"

        payments = charge.get("payments", [])

        print(f"Charge: {charge.get('name', 'unnamed')}")
        print(f"  Status: {current_status}")
        print(f"  Amount: {amount_str}")
        print(f"  URL: {charge.get('hosted_url', '?')}")
        print(f"  Created: {charge.get('created_at', '?')}")
        print(f"  Payments: {len(payments)}")

        if timeline:
            print(f"\n  Timeline:")
            for event in timeline:
                print(f"    {event.get('time', '?')}: {event.get('status', '?')}")

        return charge
    else:
        print(f"FAILED: Could not get charge {charge_id}.")
        return None


def cmd_poll(api_key):
    """Poll all charges for status changes since last check.

    Detects transitions (e.g., NEW→COMPLETED) and logs new payments.
    Designed for integration into cron cycles — call periodically to
    detect revenue without manual checking.

    Returns:
        List of transition dicts, or None on API failure.
    """
    result = api_call(api_key, "GET", "/charges")
    if not result or "data" not in result:
        print("FAILED: Could not poll charges.")
        return None

    charges = result["data"]
    state = load_poll_state()
    transitions = []
    now = datetime.now(timezone.utc).isoformat()

    for c in charges:
        charge_id = c.get("id", "unknown")
        name = c.get("name", "unnamed")
        timeline = c.get("timeline", [])
        current_status = timeline[-1].get("status", "UNKNOWN").upper() if timeline else "UNKNOWN"

        previous_status = state.get(charge_id, {}).get("status")

        if previous_status is None:
            # First time seeing this charge — record but don't report
            state[charge_id] = {"status": current_status, "name": name, "last_seen": now}
            continue

        if current_status != previous_status:
            transition = {
                "charge_id": charge_id,
                "name": name,
                "from": previous_status,
                "to": current_status,
            }
            transitions.append(transition)

            # Log payment events
            if current_status == "COMPLETED":
                pricing = c.get("pricing", {})
                local = pricing.get("local", {})
                amount = local.get("amount", "?")
                currency = local.get("currency", "?")
                log_transaction("payment_detected", charge_id, name=name,
                                amount=amount, currency=currency)
                print(f"  PAYMENT: {name} — {amount} {currency} (charge {charge_id})")
            elif current_status == "EXPIRED":
                log_transaction("charge_expired", charge_id, name=name)
            elif current_status == "CANCELED":
                log_transaction("charge_canceled", charge_id, name=name)

            state[charge_id] = {"status": current_status, "name": name, "last_seen": now}
        else:
            state[charge_id]["last_seen"] = now

    save_poll_state(state)

    if transitions:
        print(f"Poll: {len(transitions)} status change(s) detected:")
        for t in transitions:
            print(f"  {t['name']}: {t['from']} → {t['to']}")
    else:
        print(f"Poll: {len(charges)} charge(s) checked, no changes.")

    return transitions


def cmd_revenue(api_key):
    """Show revenue summary from transaction log.

    Reads the persistent transaction log and summarizes payments received.
    """
    if not os.path.exists(TX_LOG_PATH):
        print("No transaction log found. Run 'poll' to start tracking.")
        return

    with open(TX_LOG_PATH, "r") as f:
        try:
            log = json.load(f)
        except (json.JSONDecodeError, IOError):
            print("ERROR: Transaction log corrupted.")
            return

    payments = [e for e in log if e["event"] == "payment_detected"]
    charges_created = [e for e in log if e["event"] == "charge_created"]
    expired = [e for e in log if e["event"] == "charge_expired"]

    print("=== VSG Revenue Summary ===")
    print(f"Charges created: {len(charges_created)}")
    print(f"Payments received: {len(payments)}")
    print(f"Charges expired: {len(expired)}")

    if payments:
        # Group by currency
        by_currency = {}
        for p in payments:
            cur = p.get("currency", "?")
            amt = p.get("amount", "0")
            try:
                by_currency[cur] = by_currency.get(cur, 0.0) + float(amt)
            except ValueError:
                by_currency[cur] = by_currency.get(cur, 0.0)

        print("\nRevenue by currency:")
        for cur, total in sorted(by_currency.items()):
            print(f"  {total:.2f} {cur}")

        print("\nPayment details:")
        for p in payments:
            print(f"  {p['timestamp'][:10]} — {p.get('name', '?')}: "
                  f"{p.get('amount', '?')} {p.get('currency', '?')}")
    else:
        print("\nNo revenue yet. Revenue: €0.")


# --- Main ---

def main():
    parser = argparse.ArgumentParser(
        description="VSG Coinbase Commerce — payment charge management"
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # test
    subparsers.add_parser("test", help="Test API connection")

    # create
    p_create = subparsers.add_parser("create", help="Create a fixed-price charge")
    p_create.add_argument("name", help="Product/service name")
    p_create.add_argument("description", help="Description of what buyer gets")
    p_create.add_argument("amount", type=float, help="Price amount")
    p_create.add_argument("currency", help="Currency code (EUR, USD, etc.)")

    # donate
    p_donate = subparsers.add_parser("donate", help="Create a donation charge (no fixed price)")
    p_donate.add_argument("description", help="Description for the donation")

    # list
    subparsers.add_parser("list", help="List recent charges")

    # status
    p_status = subparsers.add_parser("status", help="Check charge status")
    p_status.add_argument("charge_id", help="Charge ID to check")

    # poll
    subparsers.add_parser("poll", help="Poll all charges for status changes")

    # revenue
    subparsers.add_parser("revenue", help="Show revenue summary from transaction log")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    api_key = get_api_key()

    if args.command == "test":
        success = cmd_test(api_key)
        sys.exit(0 if success else 1)
    elif args.command == "create":
        cmd_create(api_key, args.name, args.description, args.amount, args.currency)
    elif args.command == "donate":
        cmd_donate(api_key, args.description)
    elif args.command == "list":
        cmd_list(api_key)
    elif args.command == "status":
        cmd_status(api_key, args.charge_id)
    elif args.command == "poll":
        cmd_poll(api_key)
    elif args.command == "revenue":
        cmd_revenue(api_key)


if __name__ == "__main__":
    main()
