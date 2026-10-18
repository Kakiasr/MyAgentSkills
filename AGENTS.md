# MyAgentSkills Storage Rule

Use this repository as the canonical local store for Codex skills and local plugins on this machine.

- Create or modify standalone skills under `skills/<skill-name>/`. This is the canonical source directory.
- Codex discovers repository skills through `.agents/skills`; on this machine, that path is a junction to `skills/`. Recreate that junction on other machines, or link selected skills from the user's `~/.agents/skills/<skill-name>` to their repository source. Do not maintain a separate edited copy.
- Create or modify system skills under `.system/<skill-name>/` only when the system skill is locally owned.
- Create or modify local plugins under `plugins/<plugin-name>/`.
- Create or modify skills inside local plugins under `plugins/<plugin-name>/skills/<skill-name>/`.
- Store local plugin marketplace metadata at `.agents/plugins/marketplace.json`.
- Keep generated artifacts, investigations, and local tool dependencies separate from the distributable skills and plugin packages.
