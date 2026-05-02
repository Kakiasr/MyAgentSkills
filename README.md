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
