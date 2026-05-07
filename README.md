# MyAgentSkills

This repository is the local global skill store for Codex on this machine.

Canonical local path:

```text
/Users/kakiasr/Documents/MyAgentSkills
```

Codex loads user-installed skills through:

```text
/Users/kakiasr/.codex/skills
```

That path is configured as a symbolic link to this repository, so new local skills
created or installed under `$CODEX_HOME/skills` are stored here and can be synced
through Git.

Local plugin source is also stored here:

```text
/Users/kakiasr/Documents/MyAgentSkills/plugins
```

The active local plugin marketplace is stored at:

```text
/Users/kakiasr/Documents/MyAgentSkills/.agents/plugins/marketplace.json
```

Compatibility paths such as `/Users/kakiasr/plugins` and
`/Users/kakiasr/.agents/plugins/marketplace.json` should point back into this
repository.

## Automatic Git sync

This repository can auto-commit and push local skill changes.

The sync script is:

```text
/Users/kakiasr/Documents/MyAgentSkills/scripts/auto_sync_skills.sh
```

The current always-on process uses:

```text
/Users/kakiasr/Documents/MyAgentSkills/scripts/auto_sync_loop.sh
```

It checks the repository once per minute, stages all repository changes, commits
them on `main`, rebases from `origin/main`, and pushes to `origin/main`.

A macOS LaunchAgent template is also available:

```text
/Users/kakiasr/Documents/MyAgentSkills/launchd/com.kakiasr.myagentskills.autosync.plist
```

Because the repository is under `Documents`, macOS privacy controls may block
LaunchAgent access unless the executing shell has Full Disk Access. In that
case, use the loop script from an already-authorized terminal session.

Logs are written to:

```text
/Users/kakiasr/Library/Logs/MyAgentSkills/auto-sync.log
/Users/kakiasr/Library/Logs/MyAgentSkills/auto-sync-loop.log
```
