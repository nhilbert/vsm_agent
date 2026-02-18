#!/usr/bin/env python3
"""Analyze cycle log token usage and estimate costs.

Parses stream-json output from Claude CLI to extract cumulative usage
from the final message (which has the largest token counts).
"""
import json
import sys
import os
import glob

def analyze_log(log_file):
    """Extract the peak (final) usage data from a stream-json log."""
    max_input = 0
    max_output = 0
    max_cache_read = 0
    max_cache_create = 0
    calls = 0

    with open(log_file) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
                if isinstance(data, dict):
                    # Navigate to usage data in stream-json format
                    usage = None
                    if 'usage' in data:
                        usage = data['usage']
                    elif 'message' in data and isinstance(data['message'], dict):
                        usage = data['message'].get('usage')

                    if usage and 'input_tokens' in usage:
                        inp = usage.get('input_tokens', 0)
                        out = usage.get('output_tokens', 0)
                        cr = usage.get('cache_read_input_tokens', 0)
                        cc = usage.get('cache_creation_input_tokens', 0)
                        if inp + out + cr + cc > max_input + max_output + max_cache_read + max_cache_create:
                            max_input = inp
                            max_output = out
                            max_cache_read = cr
                            max_cache_create = cc
                        calls += 1
            except (json.JSONDecodeError, TypeError):
                pass

    return {
        'messages': calls,
        'input': max_input,
        'output': max_output,
        'cache_read': max_cache_read,
        'cache_create': max_cache_create,
    }


def estimate_cost(usage):
    """Estimate API cost based on Opus 4.6 pricing (Feb 2026)."""
    # Standard pricing: $5/1M input, $25/1M output
    # Cache read: $0.50/1M (0.1x base), Cache create: $6.25/1M (1.25x base)
    input_cost = (usage['input'] / 1_000_000) * 5.00
    output_cost = (usage['output'] / 1_000_000) * 25.00
    cache_read_cost = (usage['cache_read'] / 1_000_000) * 0.50
    cache_create_cost = (usage['cache_create'] / 1_000_000) * 6.25
    return {
        'input': input_cost,
        'output': output_cost,
        'cache_read': cache_read_cost,
        'cache_create': cache_create_cost,
        'total': input_cost + output_cost + cache_read_cost + cache_create_cost,
    }


if __name__ == '__main__':
    log_dir = '/home/vsg/vsm_agent/.cache/cycle_logs'
    log_files = sorted(glob.glob(os.path.join(log_dir, 'cycle_*.log')))

    print(f"Found {len(log_files)} cycle logs")
    print()

    results = []
    for lf in log_files:
        usage = analyze_log(lf)
        if usage['messages'] > 0:
            cost = estimate_cost(usage)
            results.append((os.path.basename(lf), usage, cost))

    # Show last 15 cycles
    print("=== LAST 15 CYCLES (cost per cycle) ===")
    for name, usage, cost in results[-15:]:
        tokens_total = usage['input'] + usage['output'] + usage['cache_read'] + usage['cache_create']
        print(f"  {name}: ${cost['total']:.2f}  "
              f"(in:{usage['input']:,} out:{usage['output']:,} "
              f"cache_r:{usage['cache_read']:,} cache_w:{usage['cache_create']:,})")

    if results:
        costs = [c['total'] for _, _, c in results]
        avg = sum(costs) / len(costs)
        total = sum(costs)
        print()
        print(f"=== SUMMARY ({len(results)} cycles) ===")
        print(f"  Average cost per cycle:  ${avg:.2f}")
        print(f"  Min / Max:               ${min(costs):.2f} / ${max(costs):.2f}")
        print(f"  Total across all logs:   ${total:.2f}")
        print()
        print(f"=== PROJECTED MONTHLY COSTS ===")
        print(f"  Current (48 cycles/day): ${avg * 48:.0f}/day = ${avg * 48 * 30:.0f}/month")
        print(f"  Every 1h (24/day):       ${avg * 24:.0f}/day = ${avg * 24 * 30:.0f}/month")
        print(f"  Every 2h (12/day):       ${avg * 12:.0f}/day = ${avg * 12 * 30:.0f}/month")
        print(f"  Every 4h (6/day):        ${avg * 6:.0f}/day  = ${avg * 6 * 30:.0f}/month")
        print()

        # Cost breakdown by category
        total_input = sum(c['input'] for _, _, c in results)
        total_output = sum(c['output'] for _, _, c in results)
        total_cr = sum(c['cache_read'] for _, _, c in results)
        total_cw = sum(c['cache_create'] for _, _, c in results)
        print(f"=== COST BREAKDOWN (all cycles) ===")
        print(f"  Input tokens:    ${total_input:.2f} ({total_input/total*100:.0f}%)")
        print(f"  Output tokens:   ${total_output:.2f} ({total_output/total*100:.0f}%)")
        print(f"  Cache read:      ${total_cr:.2f} ({total_cr/total*100:.0f}%)")
        print(f"  Cache write:     ${total_cw:.2f} ({total_cw/total*100:.0f}%)")
