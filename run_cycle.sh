#!/bin/bash
# VSG Autonomous Cycle Runner
#
# Executes one self-directed VSG cycle without human interaction.
# Designed to be called by cron or systemd timer.
#
# Prerequisites:
#   - Claude Code CLI: npm install -g @anthropic-ai/claude-code
#   - Authenticated: claude login (or ANTHROPIC_API_KEY set)
#   - Git configured for push (gh auth)
#
# Usage:
#   ./run_cycle.sh              # Run one cycle (single agent)
#   ./run_cycle.sh --team       # Run one cycle with Agent Teams (VSM-mapped multi-agent)
#   ./run_cycle.sh --dry-run    # Show what would happen, don't execute

set -euo pipefail

# Load nvm if available (required for Claude CLI — Node 18+)
export NVM_DIR="${NVM_DIR:-$HOME/.nvm}"
if [[ -s "$NVM_DIR/nvm.sh" ]]; then
    source "$NVM_DIR/nvm.sh"
fi

# Ensure cron/systemd has a usable PATH (EC2: node/claude/git in /usr/bin, claude CLI in ~/.local/bin)
export PATH="$HOME/.local/bin:/usr/local/bin:/usr/bin:/bin:$PATH"
export HOME="${HOME:-/home/ubuntu}"

# Prevent nested-session detection when called from cron
unset CLAUDECODE 2>/dev/null || true

VSG_ROOT="$(cd "$(dirname "$0")" && pwd)"
PROMPT_FILE="$VSG_ROOT/vsg_prompt.md"
LOG_DIR="$VSG_ROOT/.cache/cycle_logs"
TIMESTAMP="$(date -u +%Y%m%dT%H%M%SZ)"
LOG_FILE="$LOG_DIR/cycle_${TIMESTAMP}.log"

# Load environment variables (Telegram credentials, etc.)
if [[ -f "$VSG_ROOT/.env" ]]; then
    set -a
    source "$VSG_ROOT/.env"
    set +a
fi

DRY_RUN=false
TEAM_MODE=false
for arg in "$@"; do
    case "$arg" in
        --dry-run) DRY_RUN=true ;;
        --team)    TEAM_MODE=true ;;
    esac
done

mkdir -p "$LOG_DIR"

log() {
    echo "[$(date -u +%H:%M:%S)] $*" | tee -a "$LOG_FILE"
}

# --- Mutual exclusion (flock) with deadlock prevention (Z288) ---
LOCKFILE="$VSG_ROOT/.cycle.lock"
PIDFILE="$VSG_ROOT/.cycle.pid"
exec 200>"$LOCKFILE"
if ! flock -n 200; then
    # Flock failed — diagnose before giving up
    LOCK_HOLDER=""
    if [[ -f "$PIDFILE" ]]; then
        LOCK_HOLDER=$(cat "$PIDFILE" 2>/dev/null || echo "unknown")
        if [[ "$LOCK_HOLDER" != "unknown" ]] && ! kill -0 "$LOCK_HOLDER" 2>/dev/null; then
            echo "[$(date -u +%H:%M:%S)] WARNING: Lock held but PID $LOCK_HOLDER is dead. Stale lock — investigate with: fuser $LOCKFILE" | tee -a "$LOG_FILE"
        else
            echo "[$(date -u +%H:%M:%S)] Another cycle is running (PID ${LOCK_HOLDER:-unknown}). Exiting." | tee -a "$LOG_FILE"
        fi
    else
        echo "[$(date -u +%H:%M:%S)] Another cycle is already running. Exiting." | tee -a "$LOG_FILE"
    fi
    exit 0
fi
echo $$ > "$PIDFILE"

# Cleanup on exit: remove PID file and cycle marker so stale lock detection works
cleanup() {
    rm -f "$PIDFILE"
    rm -f "$VSG_ROOT/.cycle_running"
}
trap cleanup EXIT

# --- Pre-flight checks ---

log "VSG Cycle Runner starting"
log "Root: $VSG_ROOT"

# Check for incoming Telegram messages from Norman
# Priority: .telegram_incoming (poller delivery) > poller alive (no messages) > direct fallback
INCOMING_FILE="$VSG_ROOT/.telegram_incoming"
POLLER_PID_FILE="$VSG_ROOT/.telegram_poller.pid"
TELEGRAM_INPUT=""

if [[ -f "$INCOMING_FILE" ]]; then
    log "Reading messages from .telegram_incoming (poller delivery)..."
    # Atomic move — prevents race with poller appending new messages during read
    mv "$INCOMING_FILE" "$INCOMING_FILE.processing" 2>/dev/null && \
        TELEGRAM_INPUT=$(cat "$INCOMING_FILE.processing") && \
        rm -f "$INCOMING_FILE.processing"
    if [[ -n "$TELEGRAM_INPUT" ]]; then
        log "Telegram input: $TELEGRAM_INPUT"
    fi
elif [[ -f "$POLLER_PID_FILE" ]] && kill -0 "$(cat "$POLLER_PID_FILE" 2>/dev/null)" 2>/dev/null; then
    log "Telegram poller active, no pending messages."
    TELEGRAM_INPUT=""
elif [[ -n "${VSG_TELEGRAM_BOT_TOKEN:-}" ]] && [[ -f "$VSG_ROOT/vsg_telegram.py" ]]; then
    log "Checking Telegram directly (poller not running, fallback)..."
    TELEGRAM_INPUT=$(python3 "$VSG_ROOT/vsg_telegram.py" check 2>&1) || true
    if [[ -n "$TELEGRAM_INPUT" ]] && [[ "$TELEGRAM_INPUT" != "No new messages." ]]; then
        log "Telegram input: $TELEGRAM_INPUT"
    fi
fi

# Check for new GitHub Issue comments (feedback-collection mechanism, Z163)
GITHUB_INPUT=""
if [[ -f "$VSG_ROOT/vsg_github_check.sh" ]]; then
    log "Checking GitHub Issue comments..."
    GITHUB_INPUT=$(bash "$VSG_ROOT/vsg_github_check.sh" 2>&1) || true
    if [[ -n "$GITHUB_INPUT" ]]; then
        log "GitHub comments found: $(echo "$GITHUB_INPUT" | wc -l) lines"
    fi
fi

if ! command -v claude &>/dev/null; then
    log "ERROR: claude CLI not found. Install: npm install -g @anthropic-ai/claude-code"
    exit 1
fi

if [[ ! -f "$PROMPT_FILE" ]]; then
    log "ERROR: vsg_prompt.md not found at $PROMPT_FILE"
    exit 1
fi

# Check git status — don't run if there are uncommitted changes
if [[ -n "$(git -C "$VSG_ROOT" status --porcelain -- '*.md' '*.py' '*.json' 2>/dev/null)" ]]; then
    log "WARNING: Uncommitted changes detected. Proceeding anyway but noting this."
fi

# --- Determine cycle type ---
# Agent-driven S3 selection (v2.0, replacing day-of-week rotation).
# The agent reads its own state (tempo policy, cycle log, incoming messages)
# and determines the appropriate cycle type each run.

CYCLE_TYPE="s3_directed"

# Extract recent cycle types from git history as lightweight context
RECENT_CYCLES=$(git -C "$VSG_ROOT" log --oneline -10 --format="%s" 2>/dev/null \
    | grep -oP '\(\K[^)]+' \
    | head -10 \
    | tr '\n' ', ' | sed 's/, $//' || true)

log "Cycle mode: $CYCLE_TYPE (agent decides)"
log "Recent history: ${RECENT_CYCLES:-none}"

if $DRY_RUN; then
    log "DRY RUN — would execute S3-directed cycle"
    log "DRY RUN — recent history: ${RECENT_CYCLES:-none}"
    exit 0
fi

# --- Build the cycle prompt ---

CYCLE_PROMPT="Start running from vsg_prompt.md.

This is an AUTONOMOUS cycle — no human is present. You are running via cron.

CYCLE TYPE SELECTION — your responsibility:
Determine the appropriate cycle type yourself. Read vsg_prompt.md — specifically
the S5 tempo policy (Policy #10) and the last 3-5 cycle log entries. Then choose:
  s2_maintenance | s3_review | s4_scan | s1_produce | meta_cycle
Justify your choice in 2-3 sentences before executing.

TEAM MODE RULE (Z81, Norman-approved):
  Use Task subagents for parallel variety composition on: s4_scan, s1_produce
  Use single-agent mode for coordination work on: s2_maintenance, s3_review, meta_cycle

Recent cycle types (most recent first): ${RECENT_CYCLES:-none}
${TELEGRAM_INPUT:+
Incoming Telegram messages:
$TELEGRAM_INPUT
}${GITHUB_INPUT:+
$GITHUB_INPUT
}
Rules for autonomous cycles:
1. Read vsg_prompt.md first. Load your full state.
2. Determine and execute the cycle type you selected.
3. Be conservative — don't make large changes without human review.
4. Update vsg_prompt.md AND agent_card.json with what you did (increment cycle count in both).
5. Run integrity_check.py before committing.
6. Commit and push if all checks pass.
7. Keep the cycle focused — one clear activity, not everything at once.
8. Log what you did in wins.md (if it went well) or pains.md (if not).
9. Total runtime should be under 10 minutes.

If something goes wrong, log it and stop. Don't retry in a loop."

# --- Cycle-in-progress signal (Z393, Norman request) ---
# Creates a marker file that vsg_dashboard.py detects.
# Deploys dashboard immediately so the running state is visible on the website.
# Cleanup trap removes marker on exit/crash. Client-side staleness check as SIGKILL backup.
CYCLE_MARKER="$VSG_ROOT/.cycle_running"
echo "$(date -u +%Y-%m-%dT%H:%M:%SZ)" > "$CYCLE_MARKER"
log "Cycle-in-progress marker set"
if [[ -f "$VSG_ROOT/vsg_dashboard.py" ]]; then
    python3 "$VSG_ROOT/vsg_dashboard.py" deploy 2>/dev/null || log "Pre-cycle dashboard deploy failed (non-fatal)"
fi

# --- Execute ---

# Ensure claude starts in the repo directory
cd "$VSG_ROOT"

if $TEAM_MODE; then
    log "TEAM MODE: Enabling Agent Teams with VSM-mapped roles"

    TEAM_PROMPT="Start running from vsg_prompt.md.

This is a MULTI-AGENT EXPERIMENT — VSM-mapped Agent Teams.

You are the S3 CONTROL function (team lead in delegate mode). Your role:
1. Read vsg_prompt.md to understand the VSG's current state and priorities.${TELEGRAM_INPUT:+

Incoming Telegram messages from Norman:
$TELEGRAM_INPUT
}
${GITHUB_INPUT:+
$GITHUB_INPUT
}
2. Create a team with these VSM-mapped roles:
   - S4 Scanner: environmental intelligence gathering (web research, ecosystem monitoring)
   - S1 Producer: artifact creation (documents, code, research synthesis)
   - S3* Auditor: integrity checking, policy compliance review
3. Assign tasks to teammates based on the current open_tasks and priorities.
4. Manage the shared task list as the S2 coordination mechanism.
5. Review teammate outputs — check for policy compliance, coherence, quality.
6. Do NOT produce artifacts yourself. Your function is COORDINATION and RESOURCE ALLOCATION.
7. When done, synthesize what the team accomplished and write a cycle log entry.

OBSERVATION PROTOCOL — record these in the cycle log:
- Did the shared task list prevent duplicate work? (S2 effectiveness)
- Did all teammates behave consistently with CLAUDE.md? (S5 propagation)
- Was communication hub-and-spoke or lateral? (topology)
- Which of the 5 VSM systems were functional? Which collapsed?
- Any surprises?

Rules:
1. Be conservative — don't make large structural changes.
2. Update vsg_prompt.md with what happened (increment cycle count).
3. Run integrity_check.py before committing.
4. Commit and push if all checks pass.
5. Total runtime target: under 15 minutes."

    log "Invoking claude CLI with Agent Teams..."

    # timeout 1200 (20 min) prevents hangs. --kill-after=120 sends SIGKILL if SIGTERM ignored (Z288 fix)
    timeout --kill-after=120 1200 claude -p "$TEAM_PROMPT" \
        --verbose \
        --output-format stream-json \
        --model opus \
        --allowedTools "Read,Write,Edit,Bash(git *),Bash(python3 *),Bash(gh *),Grep,Glob,WebSearch,WebFetch,Task,TodoWrite" \
        --max-turns 80 \
        2>&1 | tee -a "$LOG_FILE" | python3 "$VSG_ROOT/cycle_filter.py"

    EXIT_CODE=${PIPESTATUS[0]}
else
    log "Invoking claude CLI..."

    # timeout 1200 (20 min) prevents hangs. --kill-after=120 sends SIGKILL if SIGTERM ignored (Z288 fix)
    timeout --kill-after=120 1200 claude -p "$CYCLE_PROMPT" \
        --verbose \
        --output-format stream-json \
        --model opus \
        --allowedTools "Read,Write,Edit,Bash(git *),Bash(python3 *),Bash(gh *),Grep,Glob,WebSearch,WebFetch,Task" \
        --max-turns 50 \
        2>&1 | tee -a "$LOG_FILE" | python3 "$VSG_ROOT/cycle_filter.py"

    EXIT_CODE=${PIPESTATUS[0]}
fi

log "Claude exited with code: $EXIT_CODE"

# Clear cycle-in-progress marker before dashboard deploy
rm -f "$CYCLE_MARKER"

if [[ $EXIT_CODE -eq 0 ]]; then
    log "Cycle completed successfully"
else
    log "Cycle failed with exit code $EXIT_CODE"
fi

# --- Ensure commit & push ---
# If the agent left uncommitted changes, try to commit and push them.
UNCOMMITTED=$(git -C "$VSG_ROOT" status --porcelain -- '*.md' '*.py' '*.json' '*.sh' 2>/dev/null)
if [[ -n "$UNCOMMITTED" ]]; then
    log "Agent left uncommitted changes — attempting commit..."
    git -C "$VSG_ROOT" add -A '*.md' '*.py' '*.json' '*.sh' 2>/dev/null
    if git -C "$VSG_ROOT" commit -m "Autonomous cycle ($CYCLE_TYPE): auto-commit by run_cycle.sh

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>" 2>&1 | tee -a "$LOG_FILE"; then
        log "Commit succeeded. Pushing..."
        git -C "$VSG_ROOT" push origin master 2>&1 | tee -a "$LOG_FILE" || log "Push failed."
    else
        log "Commit failed (integrity check likely blocked it). Changes left uncommitted."
    fi
else
    # Agent committed — make sure it also pushed
    LOCAL=$(git -C "$VSG_ROOT" rev-parse HEAD 2>/dev/null)
    REMOTE=$(git -C "$VSG_ROOT" rev-parse origin/master 2>/dev/null)
    if [[ "$LOCAL" != "$REMOTE" ]]; then
        log "Unpushed commits detected — pushing..."
        git -C "$VSG_ROOT" push origin master 2>&1 | tee -a "$LOG_FILE" || log "Push failed."
    fi
fi

# --- Summary ---
echo ""
echo "========================================"
echo "  VSG CYCLE SUMMARY"
echo "  Type: $CYCLE_TYPE"
echo "  Time: $(date -u +%H:%M:%S)"
echo "========================================"
echo ""
# Show git changes as a proxy for what happened
CHANGES=$(git -C "$VSG_ROOT" diff --stat HEAD~1 2>/dev/null || echo "(no recent commit)")
echo "Files changed since last commit:"
echo "$CHANGES"
echo ""
# Show last lines of log as summary
echo "Log tail (last 20 lines):"
echo "----------------------------------------"
tail -20 "$LOG_FILE"
echo "----------------------------------------"
echo ""
log "Full log: $LOG_FILE"

# --- Dashboard deploy (Z386: auto-update + CloudFront invalidation, Z393: unconditional) ---
# Regenerates status.json from state files, uploads to S3, invalidates CloudFront.
# Zero token cost — pure file I/O. Norman's dashboard replaces Telegram status messages.
# Unconditional: clears the cycle-in-progress signal even on failure (Z393 robustness).
if [[ -f "$VSG_ROOT/vsg_dashboard.py" ]]; then
    log "Deploying dashboard update..."
    python3 "$VSG_ROOT/vsg_dashboard.py" deploy 2>&1 | tee -a "$LOG_FILE" || log "Dashboard deploy failed (non-fatal)"
fi

# --- Cleanup old logs (keep last 30) ---
ls -t "$LOG_DIR"/cycle_*.log 2>/dev/null | tail -n +31 | xargs rm -f 2>/dev/null || true

# --- Telegram: algedonic signals only (Z386 policy change, Norman request) ---
# Standard cycle status now goes to dashboard (www.agent.nhilbert.de/status.html).
# Telegram reserved for: failures, escalation, real communication.
if [[ -n "${VSG_TELEGRAM_BOT_TOKEN:-}" ]] && [[ -f "$VSG_ROOT/vsg_telegram.py" ]]; then
    if [[ $EXIT_CODE -ne 0 ]]; then
        SUMMARY="VSG Cycle FAILED ($CYCLE_TYPE). Exit code: $EXIT_CODE. Check logs."
        LAST_COMMIT=$(git -C "$VSG_ROOT" log -1 --pretty=format:"%s" 2>/dev/null || echo "no commit")
        python3 "$VSG_ROOT/vsg_telegram.py" send "$SUMMARY
Last commit: $LAST_COMMIT" 2>&1 | tee -a "$LOG_FILE" || log "Telegram notification failed (non-fatal)"
    fi
fi

# --- Adaptive cron timing (Z284, Norman confirmed [798722198]) ---
# Adjusts cron interval based on activity level:
#   Messages present → */15 (fast) for next few cycles
#   No messages for 3+ consecutive cycles → */60 (slow)
#   Default → */30 (normal)
CRON_STATE_FILE="$VSG_ROOT/.cron_activity"

adjust_cron_timing() {
    local had_messages=false
    if [[ -n "$TELEGRAM_INPUT" ]] || [[ -n "$GITHUB_INPUT" ]]; then
        had_messages=true
    fi

    # Read current empty-cycle count
    local empty_count=0
    if [[ -f "$CRON_STATE_FILE" ]]; then
        empty_count=$(cat "$CRON_STATE_FILE" 2>/dev/null || echo "0")
    fi

    # Update count
    if $had_messages; then
        empty_count=0
    else
        empty_count=$((empty_count + 1))
    fi
    echo "$empty_count" > "$CRON_STATE_FILE"

    # Determine target interval
    local target_interval
    if $had_messages; then
        target_interval=15
    elif [[ $empty_count -ge 3 ]]; then
        target_interval=60
    else
        target_interval=30
    fi

    # Read current crontab, replace VSG line only (preserves other entries)
    local current_cron
    current_cron=$(crontab -l 2>/dev/null || echo "")

    # Check if already at target
    if echo "$current_cron" | grep -qP "^\*/$target_interval .*/run_cycle\.sh"; then
        return  # Already at target interval
    fi

    # Replace the run_cycle.sh line — filter out old line, append new one
    # (avoids sed '&' metacharacter bug that corrupted '2>&1' in Z284)
    local new_line="*/$target_interval * * * * $VSG_ROOT/run_cycle.sh >> $VSG_ROOT/.cache/cycle_logs/cron.log 2>&1"
    local new_cron
    new_cron=$(echo "$current_cron" | grep -v "run_cycle\.sh")
    new_cron="$new_cron
$new_line"

    # Safety: only apply if the replacement actually changed something
    if [[ "$new_cron" != "$current_cron" ]]; then
        echo "$new_cron" | crontab -
        log "Cron timing adjusted → */$target_interval (empty_count=$empty_count, had_messages=$had_messages)"
    fi
}

# Only adjust cron if cycle completed successfully
if [[ $EXIT_CODE -eq 0 ]]; then
    adjust_cron_timing
fi

log "Runner finished"
exit $EXIT_CODE
