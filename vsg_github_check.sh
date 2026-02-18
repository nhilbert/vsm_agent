#!/bin/bash
# VSG GitHub Issue Comment Checker
#
# Checks for new comments on the repo's GitHub Issues since the last check.
# Uses a timestamp file (.github_comments_seen) to track what's been seen.
#
# Usage:
#   ./vsg_github_check.sh           # Output new comments (if any)
#   ./vsg_github_check.sh --init    # Initialize timestamp to now (mark all as seen)
#
# Output: Formatted comment text for inclusion in cycle prompt, or empty string.
# Exit codes: 0 = success, 1 = error (gh not available, API failure)

set -euo pipefail

VSG_ROOT="$(cd "$(dirname "$0")" && pwd)"
SEEN_FILE="$VSG_ROOT/.github_comments_seen"
REPO="nhilbert/vsm_agent"

# Check prerequisites
if ! command -v gh &>/dev/null; then
    echo "" # Silent failure — gh not available
    exit 0
fi

# Initialize mode — mark all current comments as seen
if [[ "${1:-}" == "--init" ]]; then
    date -u +%Y-%m-%dT%H:%M:%SZ > "$SEEN_FILE"
    echo "Initialized: all comments before $(cat "$SEEN_FILE") marked as seen."
    exit 0
fi

# Determine the cutoff timestamp
if [[ -f "$SEEN_FILE" ]]; then
    SINCE=$(cat "$SEEN_FILE")
else
    # First run: only show comments from the last 24 hours to avoid flooding
    SINCE=$(date -u -d '24 hours ago' +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u +%Y-%m-%dT%H:%M:%SZ)
fi

# Fetch comments since the cutoff
# gh api returns comments sorted by created_at ascending
COMMENTS=$(gh api "repos/$REPO/issues/comments?since=$SINCE&per_page=100" \
    --jq '.[] | select(.user.login != "github-actions[bot]") | "Issue #\(.issue_url | split("/") | last) [\(.user.login), \(.created_at)]:\n\(.body)\n---"' \
    2>/dev/null) || {
    echo "" # API failure — silent, don't block the cycle
    exit 0
}

if [[ -z "$COMMENTS" ]]; then
    echo "" # No new comments
    exit 0
fi

# Update the seen timestamp to now
date -u +%Y-%m-%dT%H:%M:%SZ > "$SEEN_FILE"

# Output formatted for cycle prompt
echo "GitHub Issue comments (new since last check):"
echo "$COMMENTS"
