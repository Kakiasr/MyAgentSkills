import { spawn } from 'node:child_process';
import { createInterface } from 'node:readline';
import { join } from 'node:path';
import { pluginRoot, reaVersion } from './runtime.mjs';

// Exercise the packaged launcher itself, not just the REA executable.
const child = spawn(process.execPath, [join(pluginRoot, 'scripts', 'launch.mjs'), 'mcp'], {
  stdio: ['pipe', 'pipe', 'pipe'], windowsHide: true,
});
let sequence = 0;
const pending = new Map();
let stderr = '';
child.stderr.on('data', data => { stderr = (stderr + data).slice(-8000); });
const lines = createInterface({ input: child.stdout });
lines.on('line', line => {
  try {
    const message = JSON.parse(line);
    const callback = pending.get(message.id);
    if (callback) {
      pending.delete(message.id);
      message.error ? callback.reject(new Error(JSON.stringify(message.error))) : callback.resolve(message.result);
    }
  } catch (error) {
    for (const callback of pending.values()) callback.reject(error);
  }
});
child.on('error', error => { for (const callback of pending.values()) callback.reject(error); });
child.on('exit', () => { for (const callback of pending.values()) callback.reject(new Error(`Server exited: ${stderr}`)); });
function request(method, params) {
  return new Promise((resolve, reject) => {
    const id = ++sequence;
    pending.set(id, { resolve, reject });
    child.stdin.write(JSON.stringify({ jsonrpc: '2.0', id, method, params }) + '\n');
  });
}
const timeout = setTimeout(() => {
  for (const callback of pending.values()) callback.reject(new Error('MCP verification timed out'));
  child.stdin.end();
  child.kill();
}, 30000);
try {
  const init = await request('initialize', { protocolVersion: '2025-11-25', capabilities: {}, clientInfo: { name: 'rea-local-package-verifier', version: '0.2.0' } });
  if (init.serverInfo.version !== reaVersion) throw new Error('Server version mismatch');
  child.stdin.write(JSON.stringify({ jsonrpc: '2.0', method: 'notifications/initialized' }) + '\n');
  let cursor;
  const tools = [];
  do {
    const page = await request('tools/list', cursor ? { cursor } : {});
    tools.push(...page.tools);
    cursor = page.nextCursor;
  } while (cursor);
  if (tools.length !== 207 || !tools.some(tool => tool.name === 'binary_session')) throw new Error('Tool inventory mismatch');
  const response = await request('tools/call', { name: 'binary_session', arguments: {} });
  if (response.isError) throw new Error('binary_session failed');
  console.log(JSON.stringify({ healthy: true, version: init.serverInfo.version, tools: tools.length, request: 'binary_session', launcher: 'verified' }, null, 2));
} catch (error) {
  console.error(error.message);
  process.exitCode = 1;
} finally {
  clearTimeout(timeout);
  child.stdin.end();
  lines.close();
  child.kill();
}
