#!/usr/bin/env bash
set -euo pipefail

SYNC_SCRIPT="/Users/kakiasr/Documents/MyAgentSkills/scripts/auto_sync_skills.sh"
LOG_DIR="$HOME/Library/Logs/MyAgentSkills"
LOOP_LOG="$LOG_DIR/auto-sync-loop.log"
INTERVAL_SECONDS="${MYAGENTSKILLS_SYNC_INTERVAL_SECONDS:-60}"

mkdir -p "$LOG_DIR"

log() {
  printf '[%s] %s\n' "$(date '+%Y-%m-%d %H:%M:%S %z')" "$*" >>"$LOOP_LOG"
}

log "Starting auto-sync loop with interval ${INTERVAL_SECONDS}s."

while true; do
  if ! "$SYNC_SCRIPT"; then
    log "Sync run failed; see $LOG_DIR/auto-sync.log for details."
  fi

  sleep "$INTERVAL_SECONDS"
done
