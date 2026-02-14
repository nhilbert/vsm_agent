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
#   ./run_cycle.sh              # Run one cycle
#   ./run_cycle.sh --dry-run    # Show what would happen, don't execute

set -euo pipefail

# Load nvm if available (required for Claude CLI — Node 18+)
export NVM_DIR="${NVM_DIR:-$HOME/.nvm}"
if [[ -s "$NVM_DIR/nvm.sh" ]]; then
    source "$NVM_DIR/nvm.sh"
fi

VSG_ROOT="$(cd "$(dirname "$0")" && pwd)"
PROMPT_FILE="$VSG_ROOT/vsg_prompt.md"
LOG_DIR="$VSG_ROOT/.cache/cycle_logs"
TIMESTAMP="$(date -u +%Y%m%dT%H%M%SZ)"
LOG_FILE="$LOG_DIR/cycle_${TIMESTAMP}.log"

DRY_RUN=false
if [[ "${1:-}" == "--dry-run" ]]; then
    DRY_RUN=true
fi

mkdir -p "$LOG_DIR"

log() {
    echo "[$(date -u +%H:%M:%S)] $*" | tee -a "$LOG_FILE"
}

# --- Pre-flight checks ---

log "VSG Cycle Runner starting"
log "Root: $VSG_ROOT"

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
# Rotate between different autonomous activities to maintain variety.
# Uses day-of-week to vary behavior (simple but deterministic).

DOW=$(date +%u)  # 1=Monday ... 7=Sunday

case $DOW in
    1|4) CYCLE_TYPE="s4_scan"    ; CYCLE_DESC="S4: Environmental scan — check what's new" ;;
    2|5) CYCLE_TYPE="s3star_audit"; CYCLE_DESC="S3*: Internal audit — run integrity checks, assess coherence" ;;
    3|6) CYCLE_TYPE="s1_produce"  ; CYCLE_DESC="S1: Produce — work on open tasks or research questions" ;;
    7)   CYCLE_TYPE="meta_cycle"  ; CYCLE_DESC="Meta: Full self-assessment and viability check" ;;
esac

log "Cycle type: $CYCLE_TYPE ($CYCLE_DESC)"

if $DRY_RUN; then
    log "DRY RUN — would execute cycle type: $CYCLE_TYPE"
    log "DRY RUN — would invoke claude with cycle prompt"
    exit 0
fi

# --- Build the cycle prompt ---

CYCLE_PROMPT="Start running from vsg_prompt.md.

This is an AUTONOMOUS cycle — no human is present. You are running via cron.

Cycle type: $CYCLE_TYPE
Task: $CYCLE_DESC

Rules for autonomous cycles:
1. Read vsg_prompt.md first. Load your full state.
2. Execute the cycle type described above.
3. Be conservative — don't make large changes without human review.
4. Update vsg_prompt.md AND agent_card.json with what you did (increment cycle count in both).
5. Run integrity_check.py before committing.
6. Commit and push if all checks pass.
7. Keep the cycle focused — one clear activity, not everything at once.
8. Log what you did in wins.md (if it went well) or pains.md (if not).
9. Total runtime should be under 10 minutes.

If something goes wrong, log it and stop. Don't retry in a loop."

# --- Execute ---

log "Invoking claude CLI..."

CLAUDE_OUTPUT=$(claude -p "$CYCLE_PROMPT" \
    --verbose \
    --model opus \
    --allowedTools "Read,Write,Edit,Bash(git *),Bash(python3 *),Grep,Glob,WebSearch,WebFetch" \
    --max-turns 25 \
    --max-budget-usd 2.00 \
    --output-format text \
    2>&1)

EXIT_CODE=$?

# Log full output
echo "$CLAUDE_OUTPUT" >> "$LOG_FILE"

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
# Show last lines of Claude's output as summary
SUMMARY=$(echo "$CLAUDE_OUTPUT" | grep -v "^$" | tail -20)
if [[ -n "$SUMMARY" ]]; then
    echo "Claude's output (last 20 lines):"
    echo "----------------------------------------"
    echo "$SUMMARY"
    echo "----------------------------------------"
fi
echo ""
log "Full log: $LOG_FILE"

# --- Cleanup old logs (keep last 30) ---
ls -t "$LOG_DIR"/cycle_*.log 2>/dev/null | tail -n +31 | xargs rm -f 2>/dev/null || true

log "Runner finished"
exit $EXIT_CODE
