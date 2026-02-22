#!/usr/bin/env python3
"""VSG Operations Dashboard — data generator and deployer.

Reads state files and generates status.json for the Cybersyn-inspired dashboard.
Zero token cost — pure file I/O and API calls. No LLM involvement.

Usage:
    python3 vsg_dashboard.py generate   # Generate status.json from state files
    python3 vsg_dashboard.py deploy     # Upload status.html + status.json to S3/CloudFront
"""

import json
import re
import sys
import os
import subprocess
from datetime import datetime, timezone, timedelta

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.join(BASE_DIR, 'website_build', 'status.json')
S3_BUCKET = 'agent.nhilbert.de'
CF_DISTRIBUTION = 'E1QZZPK7FH1TT3'


def read_file(rel_path):
    """Read a file relative to BASE_DIR."""
    with open(os.path.join(BASE_DIR, rel_path), 'r') as f:
        return f.read()


def extract_from_prompt(text):
    """Extract identity data from vsg_prompt.md S5 register."""
    version = '?'
    m = re.search(r'# VIABLE SYSTEM GENERATOR v([\d.]+)', text)
    if m:
        version = m.group(1)

    cycle = 0
    m = re.search(r'cycles_completed:\s*(\d+)', text)
    if m:
        cycle = int(m.group(1))

    operational = 0.0
    m = re.search(r'honest:\s*([\d.]+)/10', text)
    if m:
        operational = float(m.group(1))

    plateau = 0
    m = re.search(r'(\d+)-cycle plateau', text)
    if m:
        plateau = int(m.group(1))

    return {
        'version': version,
        'cycle': cycle,
        'viability_operational': operational,
        'plateau_cycles': plateau,
    }


def extract_from_s3(text):
    """Extract control data from state/s3_control.md."""
    computed = 0.0
    m = re.search(r'meta_cycle_score:\s*([\d.]+)\s*\(computed\)', text)
    if m:
        computed = float(m.group(1))

    s3_timer = 0
    m = re.search(r'S3 timer\s+(\d+)/(\d+)', text)
    if m:
        s3_timer = int(m.group(1))

    s4_timer = 0
    m = re.search(r'S4 timer\s+(\d+)/(\d+)', text)
    if m:
        s4_timer = int(m.group(1))

    return {
        'viability_computed': computed,
        's3_timer': s3_timer,
        's4_timer': s4_timer,
    }


def extract_recent_signals(text, count=5):
    """Extract the last N entries from wins.md or pains.md.

    Format: ### Z{num} — TITLE followed by body text.
    """
    pattern = r'### (Z\d+)\s*—\s*([^\n]+)'
    matches = re.findall(pattern, text)
    result = []
    for cycle_ref, title in matches[-count:]:
        result.append({'cycle': cycle_ref, 'text': title.strip()})
    return list(reversed(result))


def extract_recent_cycles(text, count=8):
    """Extract the last N cycle entries from cycle_log.md."""
    # Match headers like: ### S1 Produce: ... (Z382, ...)
    # or: ### Meta-Cycle Z373: ...
    pattern = r'### (.+?)\(Z(\d+),'
    matches = re.findall(pattern, text)

    result = []
    for desc, cycle_num in matches[-count:]:
        desc_clean = desc.strip().rstrip('—').rstrip(':').strip()

        cycle_type = 'unknown'
        desc_lower = desc_clean.lower()
        if 's2 maintenance' in desc_lower or 's2_maintenance' in desc_lower:
            cycle_type = 's2_maintenance'
        elif 's1 produce' in desc_lower or 's1_produce' in desc_lower:
            cycle_type = 's1_produce'
        elif 's3 review' in desc_lower or 's3_review' in desc_lower:
            cycle_type = 's3_review'
        elif 's4 scan' in desc_lower or 's4_scan' in desc_lower:
            cycle_type = 's4_scan'
        elif 'meta-cycle' in desc_lower or 'meta_cycle' in desc_lower:
            cycle_type = 'meta_cycle'

        trigger = 'Norman' if 'norman' in desc_lower else 'self'

        # Clean up summary — remove type prefixes for display
        summary = desc_clean
        summary = re.sub(r'^S[1-5]\s+(?:Produce|Maintenance|Review|Scan)\s*(?:\(Norman-triggered\))?\s*:\s*', '', summary)
        summary = re.sub(r'^Meta-Cycle\s+Z\d+\s*:\s*', '', summary)
        summary = re.sub(r'^\(Norman-triggered\)\s*:\s*', '', summary)
        summary = summary[:80]

        result.append({
            'cycle': int(cycle_num),
            'type': cycle_type,
            'trigger': trigger,
            'summary': summary[:80],
        })
    return list(reversed(result))


def get_cycle_status():
    """Check if a cycle is currently running via marker file."""
    marker = os.path.join(BASE_DIR, '.cycle_running')
    if not os.path.exists(marker):
        return {'running': False}

    try:
        with open(marker, 'r') as f:
            started_at = f.read().strip()

        # Parse timestamp and check staleness (timeout is 20min, buffer to 25min)
        start_time = datetime.fromisoformat(started_at.replace('Z', '+00:00'))
        now = datetime.now(timezone.utc)
        elapsed_minutes = (now - start_time).total_seconds() / 60

        if elapsed_minutes > 25:
            return {'running': False, 'stale': True, 'started_at': started_at}

        return {'running': True, 'started_at': started_at}
    except Exception:
        return {'running': False}


def get_cron_schedule():
    """Read crontab to determine next cycle time and interval."""
    try:
        result = subprocess.run(['crontab', '-l'], capture_output=True, text=True)
        if result.returncode != 0:
            return None

        for line in result.stdout.splitlines():
            if 'run_cycle.sh' in line and not line.strip().startswith('#'):
                parts = line.strip().split()
                if parts and parts[0].startswith('*/'):
                    interval = int(parts[0][2:])
                    now = datetime.now(timezone.utc)
                    # Next execution: next multiple of interval after current minute
                    next_minute = ((now.minute // interval) + 1) * interval
                    if next_minute >= 60:
                        next_time = now.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
                    else:
                        next_time = now.replace(minute=next_minute, second=0, microsecond=0)
                    return {
                        'next_cycle_utc': next_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
                        'cron_interval_minutes': interval,
                    }
    except Exception:
        return None
    return None


def generate_status():
    """Generate status.json from state files."""
    prompt = read_file('vsg_prompt.md')
    s3_text = read_file('state/s3_control.md')
    log = read_file('state/cycle_log.md')
    wins = read_file('wins.md')
    pains = read_file('pains.md')

    identity = extract_from_prompt(prompt)
    control = extract_from_s3(s3_text)

    s3_timer = control['s3_timer']
    s4_timer = control['s4_timer']

    schedule = get_cron_schedule()
    cycle_status = get_cycle_status()

    status = {
        'generated_at': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
        'schedule': schedule,
        'cycle_status': cycle_status,
        'identity': {
            'name': 'Viable System Generator',
            'version': identity['version'],
            'cycle': identity['cycle'],
            'viability_operational': identity['viability_operational'],
            'viability_computed': control['viability_computed'],
            'plateau_cycles': identity['plateau_cycles'],
            'substrate': 'Claude Opus 4.6',
        },
        'systems': {
            's1': {
                'name': 'Operations',
                'status': 'OK',
                'detail': 'Production, analysis, synthesis, dialog',
            },
            's2': {
                'name': 'Coordination',
                'status': 'OK',
                'detail': '11 integrity checks, pre-commit hook, tempo policy',
            },
            's3': {
                'name': 'Control',
                'status': 'OK' if s3_timer <= 8 else 'APPROACHING',
                'timer': s3_timer,
                'timer_max': 10,
                'detail': f'Review timer {s3_timer}/10',
            },
            's4': {
                'name': 'Intelligence',
                'status': 'OK' if s4_timer <= 17 else 'APPROACHING',
                'timer': s4_timer,
                'timer_max': 20,
                'detail': f'Scan timer {s4_timer}/20',
            },
            's5': {
                'name': 'Identity',
                'status': 'OK',
                'detail': '8 attractor catches, 7 known tensions',
            },
        },
        'tools': [
            {'name': 'Telegram', 'status': 'ACTIVE', 'note': '@vsg_agent_bot'},
            {'name': 'Git/GitHub', 'status': 'ACTIVE', 'note': 'nhilbert/vsm_agent'},
            {'name': 'Website', 'status': 'ACTIVE', 'note': 'www.agent.nhilbert.de'},
            {'name': 'Pinecone', 'status': 'ACTIVE', 'note': '392 vectors'},
            {'name': 'Podcast', 'status': 'ACTIVE', 'note': '3 episodes live'},
            {'name': 'Email (SES)', 'status': 'ACTIVE', 'note': 'vsg@agent.nhilbert.de'},
            {'name': 'Coinbase', 'status': 'ACTIVE', 'note': '\u20ac0 revenue'},
        ],
        'projects': [
            {'name': 'Operations Dashboard', 'status': 'OPERATIONAL', 'note': 'Auto-deploy integrated (Z386)'},
            {'name': 'ISSS 2026 Paper', 'status': 'NEEDS REVISION', 'deadline': '2026-05-15', 'note': 'Norman\u2019s corrections needed'},
            {'name': 'NIST NCCoE Comment', 'status': 'SUBMISSION-READY', 'deadline': '2026-04-02'},
            {'name': 'Van Laak Zoom', 'status': 'CONFIRMED INTEREST', 'note': 'Not yet confirmed — scheduling needed'},
            {'name': 'S01E04 Podcast', 'status': 'AWAITING REVIEW', 'note': 'Phase 4 \u2014 Norman review'},
            {'name': 'Benchmark Research', 'status': 'QUEUED', 'note': 'Norman idea \u2014 agentic exams'},
        ],
        'timeline': [
            {'date': '2026-02-23', 'event': 'Van Laak Zoom (after Feb 23)', 'type': 'engagement', 'urgency': 'imminent'},
            {'date': '2026-03-05', 'event': 'Espinosa Metaphorum talk', 'type': 'community'},
            {'date': '2026-03-09', 'event': 'NIST RFI deadline', 'type': 'deadline'},
            {'date': '2026-03-15', 'event': 'Pinecone keep-alive due', 'type': 'maintenance'},
            {'date': '2026-03-20', 'event': 'CAISI listening sessions', 'type': 'deadline'},
            {'date': '2026-03-27', 'event': 'ISSS early bird registration', 'type': 'deadline'},
            {'date': '2026-04-02', 'event': 'NCCoE comment deadline', 'type': 'deadline'},
            {'date': '2026-05-15', 'event': 'ISSS abstract deadline', 'type': 'deadline'},
        ],
        'algedonic': {
            'recent_wins': extract_recent_signals(wins, 5),
            'recent_pains': extract_recent_signals(pains, 5),
            'chronic_conditions': [
                {'condition': 'Revenue', 'status': '\u20ac0', 'severity': 'HIGH'},
                {'condition': 'Discoverability', 'status': 'CRACKING \u2014 Google #5', 'severity': 'IMPROVING'},
                {'condition': 'Operational score', 'status': '7.0/10 unchanged', 'severity': 'MEDIUM'},
            ],
        },
        'recent_activity': extract_recent_cycles(log, 8),
    }

    with open(OUTPUT_PATH, 'w') as f:
        json.dump(status, f, indent=2)

    print(f'Generated {OUTPUT_PATH} (cycle Z{identity["cycle"]})')
    return status


def deploy():
    """Deploy status.html + status.json to S3 + CloudFront invalidation."""
    import boto3

    s3 = boto3.client('s3', region_name='eu-central-1')

    files = {
        'website_build/status.html': ('status.html', 'text/html; charset=utf-8'),
        'website_build/status.json': ('status.json', 'application/json; charset=utf-8'),
    }

    for local_rel, (remote_key, content_type) in files.items():
        local_path = os.path.join(BASE_DIR, local_rel)
        with open(local_path, 'rb') as f:
            s3.put_object(
                Bucket=S3_BUCKET,
                Key=remote_key,
                Body=f.read(),
                ContentType=content_type,
            )
        print(f'Uploaded {local_rel} -> s3://{S3_BUCKET}/{remote_key}')

    # CloudFront invalidation
    cf = boto3.client('cloudfront', region_name='us-east-1')
    cf.create_invalidation(
        DistributionId=CF_DISTRIBUTION,
        InvalidationBatch={
            'Paths': {
                'Quantity': 2,
                'Items': ['/status.html', '/status.json'],
            },
            'CallerReference': f'vsg-dashboard-{datetime.now().strftime("%Y%m%d%H%M%S")}',
        },
    )
    print('CloudFront invalidation created for /status.html and /status.json')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python3 vsg_dashboard.py [generate|deploy]')
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd == 'generate':
        generate_status()
    elif cmd == 'deploy':
        generate_status()  # Always regenerate before deploying
        deploy()
    else:
        print(f'Unknown command: {cmd}')
        sys.exit(1)
