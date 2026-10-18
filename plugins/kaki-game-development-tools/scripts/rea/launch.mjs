import { spawn } from 'node:child_process';
import { checkNode, checkRuntime, entrypoint, engineEnvironment } from './runtime.mjs';
try {
  checkNode();
  checkRuntime();
  const child = spawn(process.execPath, [entrypoint, ...process.argv.slice(2)], { stdio: 'inherit', windowsHide: true, env: engineEnvironment() });
  child.on('error', error => { console.error(error.message); process.exitCode = 1; });
  child.on('exit', (code, signal) => { process.exitCode = code ?? (signal ? 1 : 0); });
  for (const signal of ['SIGINT', 'SIGTERM']) process.on(signal, () => child.kill(signal));
} catch (error) {
  console.error(`Game Analysis REA: ${error.message}\nWith installation authorization, run: node scripts/rea/setup.mjs from the extracted plugin directory.`);
  process.exitCode = 1;
}
