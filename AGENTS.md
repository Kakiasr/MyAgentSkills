# MyAgentSkills Storage Rule

Use this repository as the canonical local store for Codex skills and local plugins on this machine.

- Create or modify standalone skills under `.agents/skills/<skill-name>/`. Codex discovers these skills when working in this repository.
- For standalone skills needed across projects, link each skill from the user's `~/.agents/skills/<skill-name>` to its repository source. Do not maintain a separate edited copy.
- Create or modify system skills under `.system/<skill-name>/` only when the system skill is locally owned.
- Create or modify local plugins under `plugins/<plugin-name>/`.
- Create or modify skills inside local plugins under `plugins/<plugin-name>/skills/<skill-name>/`.
- Store local plugin marketplace metadata at `.agents/plugins/marketplace.json`.
- Keep generated artifacts, investigations, and local tool dependencies separate from the distributable skills and plugin packages.
