import { homedir } from 'node:os';
import { join, dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { readFileSync } from 'node:fs';

export const pluginRoot = resolve(dirname(fileURLToPath(import.meta.url)), '..');
export const reaVersion = '6.5.0';
export const runtimeRoot = join(homedir(), '.cache', 'rea-local', reaVersion);
export const entrypoint = join(runtimeRoot, 'node_modules', 'rea-agents', 'scripts', 'rea.mjs');
export function checkNode() {
  const [major, minor] = process.versions.node.split('.').map(Number);
  if (!((major === 22 && minor >= 19) || (major === 24 && minor >= 11) || major >= 26)) {
    throw new Error(`Unsupported Node ${process.versions.node}. Use Node 24.11+ (24.x), 22.19+ (22.x), or 26+.`);
  }
}
export function checkRuntime() {
  const pkg = JSON.parse(readFileSync(join(runtimeRoot, 'node_modules', 'rea-agents', 'package.json'), 'utf8'));
  if (pkg.version !== reaVersion) throw new Error(`Expected REA ${reaVersion}, found ${pkg.version}`);
}
