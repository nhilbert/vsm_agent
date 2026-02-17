#!/bin/bash
# VSG Cycle Watcher — triggers run_cycle.sh when .telegram_incoming appears
#
# Watches for .telegram_incoming creation/modification.
# Uses inotifywait if available, otherwise falls back to 2-second poll loop.
# Debounces: waits 10s after last write before triggering.
#
# This is a dumb trigger — it sees a file and calls run_cycle.sh.
# It does not understand cycle logic. run_cycle.sh handles concurrency via flock.

set -euo pipefail

VSG_ROOT="$(cd "$(dirname "$0")" && pwd)"
INCOMING_FILE="$VSG_ROOT/.telegram_incoming"
DEBOUNCE_SECS=10

log() {
    echo "[$(date -u +%Y-%m-%d\ %H:%M:%S)] watcher: $*" >&2
}

trigger_cycle() {
    log "Triggering run_cycle.sh..."
    "$VSG_ROOT/run_cycle.sh" 2>&1 || true
    log "run_cycle.sh finished (or was locked out)."
}

# --- inotifywait mode ---
watch_inotify() {
    log "Using inotifywait mode."
    while true; do
        # Block until .telegram_incoming is created or modified
        inotifywait -qq -e create -e modify -e moved_to "$VSG_ROOT" --include '\.telegram_incoming$' 2>/dev/null

        # Debounce: wait for writes to settle
        log "Detected .telegram_incoming — debouncing ${DEBOUNCE_SECS}s..."
        while true; do
            if inotifywait -qq -t "$DEBOUNCE_SECS" -e modify "$VSG_ROOT" --include '\.telegram_incoming$' 2>/dev/null; then
                # Another write happened during debounce — restart the timer
                log "Additional write detected, resetting debounce timer..."
            else
                # inotifywait timed out — no more writes, debounce complete
                break
            fi
        done

        if [[ -f "$INCOMING_FILE" ]]; then
            trigger_cycle
        fi
    done
}

# --- Polling fallback ---
watch_poll() {
    log "inotifywait not available — using poll fallback (${DEBOUNCE_SECS}s debounce, 2s poll)."
    local last_mtime=0

    while true; do
        sleep 2

        if [[ ! -f "$INCOMING_FILE" ]]; then
            continue
        fi

        current_mtime=$(stat -c %Y "$INCOMING_FILE" 2>/dev/null || echo 0)
        if [[ "$current_mtime" -le "$last_mtime" ]]; then
            continue
        fi

        # File changed — start debounce
        log "Detected .telegram_incoming change — debouncing ${DEBOUNCE_SECS}s..."
        sleep "$DEBOUNCE_SECS"

        # Check if mtime changed again during debounce
        new_mtime=$(stat -c %Y "$INCOMING_FILE" 2>/dev/null || echo 0)
        while [[ "$new_mtime" -gt "$current_mtime" ]]; do
            log "Additional write detected, resetting debounce timer..."
            current_mtime=$new_mtime
            sleep "$DEBOUNCE_SECS"
            new_mtime=$(stat -c %Y "$INCOMING_FILE" 2>/dev/null || echo 0)
        done

        last_mtime=$new_mtime

        if [[ -f "$INCOMING_FILE" ]]; then
            trigger_cycle
        fi
    done
}

# --- Main ---
log "VSG Cycle Watcher starting (watching for $INCOMING_FILE)"

if command -v inotifywait &>/dev/null; then
    watch_inotify
else
    watch_poll
fi
