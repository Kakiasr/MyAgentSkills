// Adapted from REA Local; installs only the runtime, never host registration.
import { spawnSync } from 'node:child_process';
import { mkdirSync, existsSync } from 'node:fs';
import { isAbsolute } from 'node:path';
import { checkNode, checkRuntime, entrypoint, runtimeRoot, reaVersion } from './runtime.mjs';

function run(command, args) {
  const result = spawnSync(command, args, { stdio: 'inherit', windowsHide: true });
  if (result.error) throw result.error;
  if (result.status !== 0) throw new Error(`${command} failed (${result.status})`);
}

try {
  checkNode();
  const args = process.argv.slice(2);
  let npmCli;
  for (let index = 0; index < args.length; index++) {
    if (args[index] === '--help' && args.length === 1) {
      console.log(`node scripts/rea/setup.mjs [--npm-cli /absolute/path/to/npm-cli.js]\nInstalls REA ${reaVersion} into the game-development-tools user cache only. No global registration or engine installation.`);
      process.exit(0);
    }
    if (args[index] !== '--npm-cli' || npmCli || !args[index + 1]) throw new Error(`Unsupported or incomplete argument: ${args[index]}`);
    npmCli = args[++index];
    if (!isAbsolute(npmCli) || !existsSync(npmCli)) throw new Error('--npm-cli requires an existing absolute path');
  }
  let ready = false;
  try { checkRuntime(); ready = true; } catch {}
  if (!ready) {
    mkdirSync(runtimeRoot, { recursive: true });
    const installArgs = ['install', '--prefix', runtimeRoot, `rea-agents@${reaVersion}`, '--omit=optional', '--no-audit', '--no-fund', '--fetch-retries=2', '--fetch-timeout=30000', '--maxsockets=5'];
    console.log(`Installing REA ${reaVersion} into ${runtimeRoot}`);
    if (npmCli) run(process.execPath, [npmCli, ...installArgs]);
    else if (process.platform === 'win32') {
      if (/[\r\n"%&|<>^!]/.test(runtimeRoot)) throw new Error('Use --npm-cli for this account path.');
      run('cmd.exe', ['/d', '/s', '/c', `npm.cmd ${installArgs.map(value => `"${value}"`).join(' ')}`]);
    } else run('npm', installArgs);
  }
  checkRuntime();
  run(process.execPath, [entrypoint, 'mcp', 'doctor', '--json']);
  console.log('REA runtime ready. Host registration and plugin activation were not changed.');
} catch (error) {
  console.error(`REA runtime setup failed: ${error.message}`);
  process.exitCode = 1;
}
