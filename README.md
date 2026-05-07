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

This repository can auto-commit and push local skill changes through a macOS
LaunchAgent.

The sync script is:

```text
/Users/kakiasr/Documents/MyAgentSkills/scripts/auto_sync_skills.sh
```

The LaunchAgent template is:

```text
/Users/kakiasr/Documents/MyAgentSkills/launchd/com.kakiasr.myagentskills.autosync.plist
```

When enabled, macOS watches the repository path, waits briefly for editor save
bursts to settle, then stages all repository changes, commits them on `main`,
rebases from `origin/main`, and pushes to `origin/main`.

Logs are written to:

```text
/Users/kakiasr/Library/Logs/MyAgentSkills/auto-sync.log
```
