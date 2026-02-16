#!/usr/bin/env python3
"""Filter stream-json output from Claude CLI into readable progress lines.

Reads JSON-per-line from stdin, writes human-readable summary to stdout.
Full JSON still goes to the log file via tee (before this filter).

Usage in run_cycle.sh:
    claude -p ... --output-format stream-json 2>&1 \
        | tee -a "$LOG_FILE" \
        | python3 cycle_filter.py
"""

import json
import sys
import time

START = time.time()


def elapsed():
    m, s = divmod(int(time.time() - START), 60)
    return f"{m:02d}:{s:02d}"


def truncate(s, n=120):
    s = s.replace("\n", " ").strip()
    return s[:n] + "..." if len(s) > n else s


for line in sys.stdin:
    line = line.strip()
    if not line or not line.startswith("{"):
        # Pass through non-JSON lines (the log() output from run_cycle.sh)
        if line:
            print(line, flush=True)
        continue

    try:
        event = json.loads(line)
    except json.JSONDecodeError:
        continue

    etype = event.get("type")

    if etype == "system":
        model = event.get("model", "?")
        version = event.get("claude_code_version", "?")
        print(f"[{elapsed()}] Session started — model={model}, cli={version}", flush=True)

    elif etype == "assistant":
        content = event.get("message", {}).get("content", [])
        for block in content:
            btype = block.get("type")
            if btype == "text":
                text = block.get("text", "").strip()
                if text:
                    print(f"[{elapsed()}] {truncate(text, 200)}", flush=True)
            elif btype == "tool_use":
                name = block.get("name", "?")
                inp = block.get("input", {})
                # Show a meaningful one-liner per tool
                if name == "Read":
                    detail = inp.get("file_path", "?").split("/")[-1]
                    print(f"[{elapsed()}]   -> Read {detail}", flush=True)
                elif name == "Write":
                    detail = inp.get("file_path", "?").split("/")[-1]
                    print(f"[{elapsed()}]   -> Write {detail}", flush=True)
                elif name == "Edit":
                    detail = inp.get("file_path", "?").split("/")[-1]
                    print(f"[{elapsed()}]   -> Edit {detail}", flush=True)
                elif name == "Bash":
                    cmd = inp.get("command", "?")
                    print(f"[{elapsed()}]   -> Bash: {truncate(cmd, 80)}", flush=True)
                elif name == "Grep":
                    pat = inp.get("pattern", "?")
                    print(f"[{elapsed()}]   -> Grep '{truncate(pat, 40)}'", flush=True)
                elif name == "Glob":
                    pat = inp.get("pattern", "?")
                    print(f"[{elapsed()}]   -> Glob {pat}", flush=True)
                elif name == "WebSearch":
                    q = inp.get("query", "?")
                    print(f"[{elapsed()}]   -> WebSearch: {truncate(q, 60)}", flush=True)
                elif name == "WebFetch":
                    url = inp.get("url", "?")
                    print(f"[{elapsed()}]   -> WebFetch {truncate(url, 60)}", flush=True)
                elif name == "Task":
                    desc = inp.get("description", "?")
                    print(f"[{elapsed()}]   -> Task: {truncate(desc, 60)}", flush=True)
                else:
                    print(f"[{elapsed()}]   -> {name}", flush=True)

    elif etype == "result":
        turns = event.get("num_turns", "?")
        cost = event.get("total_cost_usd")
        duration = event.get("duration_ms")
        is_error = event.get("is_error", False)
        subtype = event.get("subtype", "")

        cost_str = f"${cost:.2f}" if cost else "?"
        dur_str = f"{duration // 1000}s" if duration else "?"

        status = "DONE" if not is_error else "ERROR"
        if subtype == "error_max_turns":
            status = "MAX TURNS"

        print(f"\n{'='*50}", flush=True)
        print(f"  {status} | {turns} turns | {dur_str} | {cost_str}", flush=True)
        print(f"{'='*50}\n", flush=True)

    # user/tool_result events are intentionally skipped (they contain the huge file dumps)
