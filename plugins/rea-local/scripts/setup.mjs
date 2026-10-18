import { spawnSync } from 'node:child_process';
import { mkdirSync, cpSync, writeFileSync, readFileSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { homedir } from 'node:os';
import { checkNode, checkRuntime, entrypoint, runtimeRoot, pluginRoot, reaVersion } from './runtime.mjs';

function run(command, args) {
  const result = spawnSync(command, args, { stdio: 'inherit', windowsHide: true });
  if (result.error) throw result.error;
  if (result.status !== 0) throw new Error(`${command} failed (${result.status})`);
}
try {
  checkNode();
  const args = process.argv.slice(2);
  if (args.includes('--help')) {
    console.log('node scripts/setup.mjs [--register] [--npm-cli /path/to/npm-cli.js]\nInstalls REA 6.5.0 in the user cache; --register installs the local Codex plugin.');
  } else {
    const npmIndex = args.indexOf('--npm-cli');
    if (npmIndex !== -1 && !args[npmIndex + 1]) throw new Error('--npm-cli requires a path');
    const npmCli = npmIndex === -1 ? null : args[npmIndex + 1];
    let ready = false;
    try { checkRuntime(); ready = true; } catch {}
    if (!ready) {
      mkdirSync(runtimeRoot, { recursive: true });
      const installArgs = ['install', '--prefix', runtimeRoot, `rea-agents@${reaVersion}`, '--omit=optional', '--no-audit', '--no-fund', '--fetch-retries=2', '--fetch-timeout=30000', '--maxsockets=5'];
      console.log(`Installing REA ${reaVersion} into ${runtimeRoot}`);
      if (npmCli) run(process.execPath, [npmCli, ...installArgs]);
      else if (process.platform === 'win32') {
        if (/[\r\n"%&|<>^]/.test(runtimeRoot)) throw new Error('Use --npm-cli for this account path.');
        run('cmd.exe', ['/d', '/s', '/c', `npm.cmd ${installArgs.map(a => `"${a}"`).join(' ')}`]);
      } else run('npm', installArgs);
    }
    checkRuntime();
    run(process.execPath, [entrypoint, 'mcp', 'doctor', '--json']);
    if (args.includes('--register')) {
      const manifest = JSON.parse(readFileSync(join(pluginRoot, 'plugin.json'), 'utf8'));
      const market = join(homedir(), '.cache', 'rea-local', 'marketplace');
      const destination = join(market, 'plugins', manifest.name);
      if (pluginRoot !== destination) {
        mkdirSync(dirname(destination), { recursive: true });
        cpSync(pluginRoot, destination, { recursive: true, dereference: true });
      }
      const catalog = join(market, '.agents', 'plugins', 'marketplace.json');
      mkdirSync(dirname(catalog), { recursive: true });
      writeFileSync(catalog, JSON.stringify({ name: 'kaki-rea-local', plugins: [{ name: manifest.name, source: { source: 'local', path: `./plugins/${manifest.name}` }, policy: { installation: 'AVAILABLE', authentication: 'ON_USE' }, category: 'Developer Tools' }] }, null, 2));
      run('codex', ['plugin', 'marketplace', 'add', market, '--json']);
      run('codex', ['plugin', 'add', `${manifest.name}@kaki-rea-local`, '--json']);
    }
    console.log('REA Local ready. Restart Codex after installing the plugin.');
  }
} catch (error) {
  console.error(`Setup failed: ${error.message}\nInstall supported Node.js with npm; make node, npm and (for --register) codex available on PATH.`);
  process.exitCode = 1;
}
