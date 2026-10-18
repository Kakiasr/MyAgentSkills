import { homedir } from 'node:os';
import { join, dirname, resolve, isAbsolute } from 'node:path';
import { fileURLToPath } from 'node:url';
import { readFileSync, existsSync, statSync } from 'node:fs';

export const pluginRoot = resolve(dirname(fileURLToPath(import.meta.url)), '../..');
export const release = JSON.parse(readFileSync(join(pluginRoot, 'scripts', 'rea', 'release.json'), 'utf8'));
export const reaVersion = release.version;
export const runtimeRoot = join(homedir(), '.cache', 'kaki-game-development-tools', 'rea', reaVersion);
export const entrypoint = join(runtimeRoot, 'node_modules', 'rea-agents', 'scripts', 'rea.mjs');
export const engineConfigPath = join(homedir(), '.cache', 'kaki-game-development-tools', 'rea', 'engines.json');
export function engineEnvironment() {
  const env = { ...process.env };
  if (!existsSync(engineConfigPath)) return env;
  const config = JSON.parse(readFileSync(engineConfigPath, 'utf8'));
  if (!config || typeof config !== 'object' || Array.isArray(config)) throw new Error('Engine configuration must be an object');
  const fields = { ghidraInstallDir: 'GHIDRA_INSTALL_DIR', javaHome: 'JAVA_HOME' };
  for (const [key, value] of Object.entries(config)) {
    if (!Object.hasOwn(fields, key) || typeof value !== 'string' || !isAbsolute(value) || !existsSync(value) || !statSync(value).isDirectory()) throw new Error(`Invalid engine configuration: ${key}`);
    env[fields[key]] = value;
  }
  return env;
}
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
