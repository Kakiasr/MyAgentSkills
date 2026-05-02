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
