import { spawn } from 'node:child_process';
import { createInterface } from 'node:readline';
import { join, isAbsolute } from 'node:path';
import { mkdirSync, writeFileSync, readFileSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { pluginRoot, reaVersion, entrypoint, checkNode, checkRuntime } from './runtime.mjs';

// Creates an owned MCP process, never binds a user's current analysis session.
const args = process.argv.slice(2);
let outputDir;
let analysis = false;
for (let i = 0; i < args.length; i++) {
  if (args[i] === '--analysis' && !analysis) analysis = true;
  else if (args[i] === '--output-dir' && !outputDir && args[i + 1] && isAbsolute(args[i + 1])) outputDir = args[++i];
  else { console.error('Usage: node scripts/rea/verify.mjs [--analysis] [--output-dir /absolute/new-directory]'); process.exit(2); }
}
checkNode();
checkRuntime();
if (outputDir) mkdirSync(outputDir); // Refuse existing output rather than overwrite evidence.
const child = spawn(process.execPath, [join(pluginRoot, 'scripts/rea/launch.mjs'), 'mcp'], {
  stdio: ['pipe', 'pipe', 'pipe'], windowsHide: true,
});
let sequence = 0;
const pending = new Map();
let stderr = '';
let terminalError;
child.stderr.on('data', data => { stderr = (stderr + data).slice(-8000); });
function fail(error) {
  terminalError = error;
  for (const item of pending.values()) item.reject(error);
  pending.clear();
}
const lines = createInterface({ input: child.stdout });
lines.on('line', line => {
  try {
    const message = JSON.parse(line);
    const callback = pending.get(message.id);
    if (callback) {
      pending.delete(message.id);
      message.error ? callback.reject(new Error(JSON.stringify(message.error))) : callback.resolve(message.result);
    }
  } catch (error) { fail(error); }
});
child.on('error', fail);
child.on('exit', () => fail(new Error(`Server exited: ${stderr}`)));
child.stdin.on('error', fail);
function request(method, params) {
  if (terminalError) return Promise.reject(terminalError);
  return new Promise((resolve, reject) => {
    const id = ++sequence;
    pending.set(id, { resolve, reject });
    child.stdin.write(JSON.stringify({ jsonrpc: '2.0', id, method, params }) + '\n');
  });
}
function unpack(response) {
  if (response.isError) throw new Error(JSON.stringify(response));
  if (response.structuredContent) return response.structuredContent;
  const text = response.content?.find(item => item.type === 'text')?.text;
  if (!text) throw new Error('Response has no structured data');
  return JSON.parse(text);
}
function save(name, value) {
  if (outputDir) writeFileSync(join(outputDir, name), JSON.stringify(value, null, 2) + '\n', { flag: 'wx' });
}
const timer = setTimeout(() => {
  fail(new Error('MCP verification timed out; not evidence that every REA capability is unavailable.'));
  child.stdin.end();
  child.kill();
}, analysis ? 55000 : 30000);
try {
  const init = await request('initialize', { protocolVersion: '2025-11-25', capabilities: {}, clientInfo: { name: 'kaki-game-analysis-verifier', version: '0.8.0' } });
  if (init.serverInfo.version !== reaVersion) throw new Error('Server version mismatch');
  child.stdin.write(JSON.stringify({ jsonrpc: '2.0', method: 'notifications/initialized' }) + '\n');
  let cursor;
  const tools = [];
  const seen = new Set();
  do {
    const page = await request('tools/list', cursor ? { cursor } : {});
    tools.push(...page.tools);
    cursor = page.nextCursor;
    if (cursor && seen.has(cursor)) throw new Error('Repeated tool cursor');
    seen.add(cursor);
  } while (cursor);
  save('tool-catalog.json', tools);
  if (!tools.some(tool => tool.name === 'binary_session')) throw new Error('Missing binary_session');
  const session = unpack(await request('tools/call', { name: 'binary_session', arguments: { expected_package_version: reaVersion, expected_server_path: entrypoint } }));
  save('session.json', session);
  const status = session.result;
  if (!status || status.server_identity?.package?.version !== reaVersion) throw new Error('Session identity missing or mismatched');
  if (status.server_identity?.alignment?.state === 'mismatch') throw new Error('Session registration identity mismatch');
  const providers = (status.analysis_provider_candidates ?? []).map(item => ({
    provider: item.provider.id, status: item.availability.status,
    reason: item.availability.reason, diagnostics: item.availability.diagnostics,
  }));
  let sample = { status: 'not_requested' };
  if (analysis) {
    const tool = tools.find(item => item.name === 'analyze_javascript_application');
    if (!tool) throw new Error('Static JavaScript tool absent');
    const path = join(pluginRoot, 'skills/game-analysis/examples/rea-smoke');
    const input = { input_path: path };
    // This fixture is two tiny known files; retain full Evidence for inspection.
    const evidence = unpack(await request('tools/call', { name: tool.name, arguments: input }));
    save('sample-analysis.json', evidence);
    if (!evidence.evidence_id || !evidence.normalized_result) throw new Error('Static analysis returned no Evidence');
    const serialized = JSON.stringify(evidence.normalized_result);
    if (!serialized.includes('main.js')) throw new Error('Fixture main.js absent from static analysis result');
    const statistics = evidence.normalized_result.statistics;
    if (statistics?.parsed_javascript_files !== 1 || statistics.parse_failures !== 0 || statistics.skipped_javascript_files !== 0) throw new Error('Fixture JavaScript was not fully parsed');
    sample = { status: 'passed', evidence_id: evidence.evidence_id,
      parent_evidence_id: evidence.normalized_result.parent_evidence_id ?? null,
      fixture_sha256: createHash('sha256').update(readFileSync(join(path, 'main.js'))).digest('hex'),
      statistics,
      scope: 'synthetic JavaScript static analysis; not original-game execution or native decompilation' };
  }
  const report = { connection: 'passed', version: reaVersion, tools: tools.length,
    server_path: status.server_identity.server.command_path, alignment: status.server_identity.alignment,
    sample_analysis: sample, native_providers: providers,
    all_capabilities_verified: false, host_session_reloaded: false };
  save('verification.json', report);
  console.log(JSON.stringify(report, null, 2));
} catch (error) {
  const report = { connection_or_analysis: 'failed', error: error.message, stderr };
  save('failure.json', report);
  console.error(JSON.stringify(report, null, 2));
  process.exitCode = 1;
} finally {
  clearTimeout(timer);
  child.stdin.end();
  lines.close();
  child.kill();
}
