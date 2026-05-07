# MyAgentSkills Storage Rule

Use this repository as the canonical local store for Codex skills and local plugins on this machine.

- Create or modify standalone skills under `/Users/kakiasr/Documents/MyAgentSkills/<skill-name>/`.
- Create or modify system skills under `/Users/kakiasr/Documents/MyAgentSkills/.system/<skill-name>/`.
- Create or modify local plugins under `/Users/kakiasr/Documents/MyAgentSkills/plugins/<plugin-name>/`.
- Create or modify skills inside local plugins under `/Users/kakiasr/Documents/MyAgentSkills/plugins/<plugin-name>/skills/<skill-name>/`.
- Store local plugin marketplace metadata at `/Users/kakiasr/Documents/MyAgentSkills/.agents/plugins/marketplace.json`.
- Treat `/Users/kakiasr/.codex/skills`, `/Users/kakiasr/Documents/Codex/shared-skills`, `/Users/kakiasr/plugins`, and `/Users/kakiasr/.agents/plugins/marketplace.json` as compatibility entry points only when they resolve back into this repository.

## Automatic Git sync

- Local skill changes in this repository are expected to be synced to
  `origin/main`.
- The macOS LaunchAgent template is stored at
  `/Users/kakiasr/Documents/MyAgentSkills/launchd/com.kakiasr.myagentskills.autosync.plist`.
- The sync script is stored at
  `/Users/kakiasr/Documents/MyAgentSkills/scripts/auto_sync_skills.sh`.
- The active background loop script is stored at
  `/Users/kakiasr/Documents/MyAgentSkills/scripts/auto_sync_loop.sh` and checks
  for changes once per minute.
- If a macOS LaunchAgent is used, remember that `Documents` access can be
  blocked by TCC unless the executing shell has Full Disk Access.
- If automatic sync fails, inspect
  `/Users/kakiasr/Library/Logs/MyAgentSkills/auto-sync.log`, then resolve the
  Git/authentication/network issue and push the local commit manually.
