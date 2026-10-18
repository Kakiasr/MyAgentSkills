# REA Local 0.2.0

可迁移的本地 Codex 插件，包含 REA 官方技能、参考资料和 MCP 启动器。
上游：https://github.com/morluto/rea 。本包是本地封装，不代表上游官方插件。

## 换电脑安装

1. 安装 Node.js 24 LTS（24.11+，包含 npm）和 Codex CLI。
2. 确认 `node --version`、`npm --version`、`codex --version` 可运行。
3. 解压本包，进入含有 `plugin.json` 的 `rea-local` 目录，执行：

```text
node scripts/setup.mjs --register
```

4. 重启 Codex，选择 REA Local。

安装器固定使用 `rea-agents@6.5.0`，安装到当前用户的 `.cache/rea-local/6.5.0`，
验证 MCP 后将插件注册到 `kaki-rea-local` 本地市场。首次安装需要网络。
无需修改用户名、盘符或 MCP JSON。Codex 启动时必须能通过 PATH 找到 Node。
支持 Node 22.x >=22.19、24.x >=24.11、26+；推荐24 LTS。

若 npm 不在 PATH，但已知其 JS 入口，可执行：

```text
node scripts/setup.mjs --npm-cli /absolute/path/to/npm-cli.js --register
```

仅安装运行时：`node scripts/setup.mjs`。
验证：`node scripts/launch.mjs mcp doctor --json`。
验证本包启动器的实际 MCP 通信：`node scripts/verify.mjs`。
命令行：`node scripts/launch.mjs --help`。
MCP 启动不会隐式安装；缺少依赖时输出安装指令。

## 包结构与更新

- `plugin.json`、`mcp.json`：使用 `${PLUGIN_ROOT}` 的可迁移配置。
- `.codex-plugin/plugin.json`、`.mcp.json`：兼容配置。
- `skills/reverse-engineer-anything/`：技能和随包参考文件。
- `scripts/`：Node 安装器、检查器与启动器。
- `LICENSE`：上游 MIT 许可证。

不打包 node_modules、用户配置、凭证或游戏文件。REA 顶层版本固定；传递依赖在首次安装时由 npm 解析并生成用户缓存中的 package-lock.json，因此不是完整离线或逐字节可复现的依赖包。
升级时同步修改脚本中 REA 版本、配套技能和插件版本，再重新运行安装器。
安装器仅维护自己的市场副本和插件注册，不修改已有独立全局 REA 注册。
从0.1.0旧版迁移时，若提示同名市场来自不同目录，先执行 `codex plugin marketplace remove kaki-rea-local`，再执行安装命令；该命令只移除市场注册，不删除旧源文件。

## 范围与限制

Windows 已实测；macOS/Linux 使用相同 Node 脚本，尚未在真实系统运行验收。
不自动安装 Ghidra、IDA、Java 等分析引擎；安装时省略可选 Frida 依赖。
MCP 自检验证握手、工具目录和无目标请求，不代表所有分析工具均可使用。
本地插件不提供云服务，普通 ChatGPT 移动对话不能凭本包直接访问电脑。
本包用于私人迁移安装，未提交公共插件目录或上传账号。
