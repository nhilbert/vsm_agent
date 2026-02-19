#!/usr/bin/env python3
"""Test Coinbase CDP API access — Z254 retry after Norman fixed IP restriction."""

import boto3
import json
import time
import secrets
import jwt
import requests

def get_credentials():
    """Retrieve CDP API credentials from AWS Secrets Manager."""
    sm = boto3.client('secretsmanager', region_name='eu-central-1')

    # Get key name (strip any surrounding quotes)
    name_secret = sm.get_secret_value(SecretId='vsg/coinbase-api-key-name')
    key_name = name_secret['SecretString'].strip().strip("'\"")

    # Get EC private key
    key_secret = sm.get_secret_value(SecretId='vsg/coinbase-api-key')
    ec_key_pem = key_secret['SecretString'].strip()

    return key_name, ec_key_pem

def build_jwt(key_name, ec_key_pem, request_method, request_path):
    """Build a JWT for Coinbase CDP API authentication."""
    uri = f"{request_method} {request_path}"

    payload = {
        "sub": key_name,
        "iss": "cdp",
        "aud": ["cdp_service"],
        "nbf": int(time.time()),
        "exp": int(time.time()) + 120,
        "uris": [uri],
    }

    headers = {
        "kid": key_name,
        "nonce": secrets.token_hex(16),
        "typ": "JWT",
    }

    token = jwt.encode(
        payload,
        ec_key_pem,
        algorithm="ES256",
        headers=headers,
    )

    return token

def test_endpoint(key_name, ec_key_pem, method, path, base_url="https://api.coinbase.com"):
    """Test a single API endpoint."""
    token = build_jwt(key_name, ec_key_pem, method, path)

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    url = f"{base_url}{path}"

    try:
        if method == "GET":
            resp = requests.get(url, headers=headers, timeout=10)
        else:
            resp = requests.post(url, headers=headers, timeout=10)

        return resp.status_code, resp.text[:500]
    except Exception as e:
        return None, str(e)

def main():
    key_name, ec_key_pem = get_credentials()
    print(f"Key name: {key_name}")
    print(f"EC key: {len(ec_key_pem)} chars")
    print()

    # Test endpoints from most privileged to least
    endpoints = [
        ("GET", "/api/v3/brokerage/accounts", "Brokerage accounts (balance query)"),
        ("GET", "/v2/accounts", "V2 accounts"),
        ("GET", "/v2/user", "V2 user profile"),
        ("GET", "/api/v3/brokerage/market/products", "Market products (public)"),
        ("GET", "/api/v3/brokerage/market/products/BTC-EUR/ticker", "BTC-EUR ticker (public)"),
    ]

    for method, path, description in endpoints:
        status, body = test_endpoint(key_name, ec_key_pem, method, path)
        status_icon = "OK" if status == 200 else f"FAIL({status})"
        print(f"[{status_icon}] {description}")
        if status != 200:
            # Show first 200 chars of error body
            print(f"    Response: {body[:200]}")
        else:
            # Show abbreviated success
            try:
                data = json.loads(body)
                if isinstance(data, dict):
                    print(f"    Keys: {list(data.keys())[:5]}")
                    # If accounts, show account info
                    if 'accounts' in data:
                        for acct in data['accounts'][:3]:
                            name = acct.get('name', acct.get('currency', 'unknown'))
                            balance = acct.get('available_balance', acct.get('balance', {}))
                            print(f"    Account: {name} — Balance: {balance}")
            except json.JSONDecodeError:
                print(f"    Body: {body[:100]}")
        print()

if __name__ == "__main__":
    main()
