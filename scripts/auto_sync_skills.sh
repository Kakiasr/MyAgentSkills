#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="/Users/kakiasr/Documents/MyAgentSkills"
BRANCH="main"
REMOTE="origin"
LOCK_DIR="${TMPDIR:-/tmp}/myagentskills-auto-sync.lock"
LOG_DIR="$HOME/Library/Logs/MyAgentSkills"
LOG_FILE="$LOG_DIR/auto-sync.log"

mkdir -p "$LOG_DIR"

log() {
  printf '[%s] %s\n' "$(date '+%Y-%m-%d %H:%M:%S %z')" "$*" >>"$LOG_FILE"
}

if ! mkdir "$LOCK_DIR" 2>/dev/null; then
  log "Another auto-sync run is active; skipping."
  exit 0
fi
trap 'rmdir "$LOCK_DIR"' EXIT

cd "$REPO_DIR"

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  log "Not a Git work tree: $REPO_DIR"
  exit 1
fi

current_branch="$(git branch --show-current)"
if [[ "$current_branch" != "$BRANCH" ]]; then
  log "Current branch is $current_branch, expected $BRANCH; skipping auto-sync."
  exit 0
fi

# Debounce file-save bursts so one editor save does not create several commits.
sleep 20

changed_summary=""

if git diff --quiet && git diff --cached --quiet && [[ -z "$(git ls-files --others --exclude-standard)" ]]; then
  log "No working tree changes; checking whether local commits need push."
else
  git add -A

  if git diff --cached --quiet; then
    log "No staged changes after git add."
  else
    changed_summary="$(git diff --cached --name-only | sed -n '1,20p' | tr '\n' ', ' | sed 's/, $//')"
    commit_message="Auto-sync skill changes $(date '+%Y-%m-%d %H:%M:%S')"

    if ! git commit -m "$commit_message" >>"$LOG_FILE" 2>&1; then
      log "Commit failed for changes: $changed_summary"
      exit 1
    fi
  fi
fi

if ! git pull --rebase "$REMOTE" "$BRANCH" >>"$LOG_FILE" 2>&1; then
  log "Pull --rebase failed after local commit. Resolve manually, then run git rebase --continue or git rebase --abort."
  exit 1
fi

if ! git push "$REMOTE" "$BRANCH" >>"$LOG_FILE" 2>&1; then
  log "Push failed after commit. Local commit is ready; run git push $REMOTE $BRANCH manually after fixing auth/network."
  exit 1
fi

if [[ -n "$changed_summary" ]]; then
  log "Synced changes: $changed_summary"
else
  log "Pushed existing local commits."
fi
