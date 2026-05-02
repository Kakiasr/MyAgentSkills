# MyAgentSkills Storage Rule

Use this repository as the canonical local store for Codex skills and local plugins on this machine.

- Create or modify standalone skills under `/Users/kakiasr/Documents/MyAgentSkills/<skill-name>/`.
- Create or modify system skills under `/Users/kakiasr/Documents/MyAgentSkills/.system/<skill-name>/`.
- Create or modify local plugins under `/Users/kakiasr/Documents/MyAgentSkills/plugins/<plugin-name>/`.
- Create or modify skills inside local plugins under `/Users/kakiasr/Documents/MyAgentSkills/plugins/<plugin-name>/skills/<skill-name>/`.
- Store local plugin marketplace metadata at `/Users/kakiasr/Documents/MyAgentSkills/.agents/plugins/marketplace.json`.
- Treat `/Users/kakiasr/.codex/skills`, `/Users/kakiasr/Documents/Codex/shared-skills`, `/Users/kakiasr/plugins`, and `/Users/kakiasr/.agents/plugins/marketplace.json` as compatibility entry points only when they resolve back into this repository.
