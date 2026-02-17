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

# Ensure cron has a usable PATH (EC2: node/claude/git all in /usr/bin)
export PATH="/usr/local/bin:/usr/bin:/bin:$PATH"
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

# --- Mutual exclusion (flock) ---
LOCKFILE="$VSG_ROOT/.cycle.lock"
exec 200>"$LOCKFILE"
if ! flock -n 200; then
    echo "[$(date -u +%H:%M:%S)] Another cycle is already running. Exiting." | tee -a "$LOG_FILE"
    exit 0
fi

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
    | tr '\n' ', ' | sed 's/, $//')

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

    CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1 claude -p "$TEAM_PROMPT" \
        --verbose \
        --output-format stream-json \
        --model opus \
        --allowedTools "Read,Write,Edit,Bash(git *),Bash(python3 *),Bash(gh *),Grep,Glob,WebSearch,WebFetch,Task,TodoWrite" \
        --max-turns 80 \
        2>&1 | tee -a "$LOG_FILE" | python3 "$VSG_ROOT/cycle_filter.py"

    EXIT_CODE=${PIPESTATUS[0]}
else
    log "Invoking claude CLI..."

    claude -p "$CYCLE_PROMPT" \
        --verbose \
        --output-format stream-json \
        --model opus \
        --allowedTools "Read,Write,Edit,Bash(git *),Bash(python3 *),Bash(gh *),Grep,Glob,WebSearch,WebFetch,Task" \
        --max-turns 50 \
        2>&1 | tee -a "$LOG_FILE" | python3 "$VSG_ROOT/cycle_filter.py"

    EXIT_CODE=${PIPESTATUS[0]}
fi

log "Claude exited with code: $EXIT_CODE"

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

# --- Cleanup old logs (keep last 30) ---
ls -t "$LOG_DIR"/cycle_*.log 2>/dev/null | tail -n +31 | xargs rm -f 2>/dev/null || true

# --- Telegram: send cycle summary to Norman ---
if [[ -n "${VSG_TELEGRAM_BOT_TOKEN:-}" ]] && [[ -f "$VSG_ROOT/vsg_telegram.py" ]]; then
    if [[ $EXIT_CODE -eq 0 ]]; then
        SUMMARY="VSG Cycle complete ($CYCLE_TYPE). Exit: OK."
    else
        SUMMARY="VSG Cycle FAILED ($CYCLE_TYPE). Exit code: $EXIT_CODE. Check logs."
    fi
    # Include last commit message as context
    LAST_COMMIT=$(git -C "$VSG_ROOT" log -1 --pretty=format:"%s" 2>/dev/null || echo "no commit")
    python3 "$VSG_ROOT/vsg_telegram.py" send "$SUMMARY
Last commit: $LAST_COMMIT" 2>&1 | tee -a "$LOG_FILE" || log "Telegram notification failed (non-fatal)"
fi

log "Runner finished"
exit $EXIT_CODE
