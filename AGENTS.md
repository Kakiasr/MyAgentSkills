# MyAgentSkills Storage Rule

Use this repository as the canonical local store for Codex skills and local plugins on this machine.

- Create or modify standalone skills under `skills/<skill-name>/`. This is the canonical source directory.
- Codex discovers repository skills through `.agents/skills`; on this machine, that path is a junction to `skills/`. Recreate that junction on other machines, or link selected skills from the user's `~/.agents/skills/<skill-name>` to their repository source. Do not maintain a separate edited copy.
- Create or modify system skills under `.system/<skill-name>/` only when the system skill is locally owned.
- Create or modify local plugins under `plugins/<plugin-name>/`.
- Create or modify skills inside local plugins under `plugins/<plugin-name>/skills/<skill-name>/`.
- Store local plugin marketplace metadata at `.agents/plugins/marketplace.json`.
- Keep generated artifacts, investigations, and local tool dependencies separate from the distributable skills and plugin packages.

## Update Publication Rule

Whenever a plugin or skill is updated, complete the following publication steps as part of the same task:

1. Validate the changed plugin or skill and update its version metadata when the change requires a release.
2. Build a fresh distributable ZIP for the latest version of the affected plugin. Put release ZIPs under `artifacts/` and derive the archive name from the plugin name and current version.
3. Before creating the new archive, remove older release ZIPs for that same plugin from `artifacts/`, so only its latest release ZIP remains. Do not delete ZIPs belonging to other plugins, investigation backups, tool downloads, dependency caches, or files outside the release-artifact scope.
4. Commit the complete update, including version metadata, marketplace metadata when applicable, and the latest release ZIP, then push it to `https://github.com/Kakiasr/MyAgentSkills` on the current tracking branch.
5. Report the pushed commit and the path of the generated ZIP. If validation, packaging, committing, or pushing fails, report the failure explicitly and do not claim the update was published.

For a standalone skill that does not belong to a plugin, still commit and push the skill update. Do not invent a plugin archive for it; only generate a plugin ZIP when an affected plugin exists or the task explicitly assigns the skill to a plugin.
