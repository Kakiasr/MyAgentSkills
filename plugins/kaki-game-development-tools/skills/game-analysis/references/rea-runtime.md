# REA运行与故障恢复

## 单一入口与版本

本插件0.7.0从官方npm发布重新部署REA 6.7.0，匹配发布包内技能metadata 42。版本与下载完整性记录在插件根`scripts/rea/release.json`，上游技能完整保存在[技术参考](upstream-rea/SKILL.md)。这是2026-10-18核实的稳定版本，不承诺以后始终最新；升级须同时核对运行时、技能参考和验收。

唯一插件服务名为`game-rea`，`mcp.json`通过`${PLUGIN_ROOT}/scripts/rea/launch.mjs`启动。运行时位于当前用户`.cache/kaki-game-development-tools/rea/6.7.0`，不再读取`.cache/rea-local`或仓库`.tools/rea-runtime`。不创建独立REA插件、全局MCP注册或第二个通用逆向技能。保留的上游setup只是技术参考，不在本插件安装流程中运行它来覆盖配置。

## 安装与可迁移性

需已有支持的Node：22.19+的22.x、24.11+的24.x或26+；特定功能可能更高。启动器不自动下载；获授权后在插件根目录执行：

```text
node scripts/rea/setup.mjs
node scripts/rea/setup.mjs --npm-cli /absolute/path/to/npm-cli.js
```

安装器只准备游戏开发工具专属缓存，不注册市场、不替换技能、不安装外部分析引擎。顶层固定版本不等于传递依赖完全离线或逐字节可复现；锁文件保存在该用户运行时目录，不能把本机node_modules塞进插件。换电脑须在该设备准备运行时并安装插件。本地stdio不提供云服务或移动端本机文件访问。

## 分层验证

0.7.1起，启动器可读取当前用户`.cache/kaki-game-development-tools/rea/engines.json`，只支持`ghidraInstallDir`和`javaHome`两个本机绝对目录。这些值仅注入REA子进程，不修改系统PATH、全局JAVA_HOME或客户端全局REA注册；文件缺失时使用原有环境。配置无效会明确失败，不静默使用其他引擎。本机路径不随插件分发，换电脑应按当地安装重建。

```json
{"ghidraInstallDir": "<本机Ghidra目录绝对路径>", "javaHome": "<本机64位JDK目录绝对路径>"}
```

```text
node scripts/rea/verify.mjs
node scripts/rea/verify.mjs --analysis
node scripts/rea/verify.mjs --analysis --output-dir /absolute/path/to/new-report-directory
```

基础模式验证实际stdio握手、目录、版本和server_identity并列出provider状态；`--analysis`进一步静态分析随包合成开箱JS样本，不执行游戏或样本业务代码。输出目录必须全新，保存完整检查结果及分析Evidence。报告只证明对应层：连接通过≠样本分析通过≠原生反编译可用≠某款游戏格式受支持。

Node／启动器错误、客户端审批、原生provider缺失、格式不支持应分别诊断；已经连接时不每次跑doctor。当前工具存在但调用受客户端策略阻止，不得重装或绕过审批；原生provider缺失时继续适用的配置／JS／托管静态工作，并单列缺口。原生反编译须按安装版本要求单独准备Ghidra与匹配的64位JDK，或已有IDA／其他受支持provider；Java 8的32位JRE不是其替代。

上游[故障参考](upstream-rea/references/connection-and-recovery.md)中的全局setup命令不适用于本插件默认修复；先核对本插件来源与缓存，不重复生成全局REA注册。不因一次工具失败下载一组无关引擎。

## 删除旧部署的边界

本次重部署移除旧独立插件、旧全局入口与旧依赖引用；旧插件源码和配置已在插件外备份。旧磁盘目录的隔离移动被执行策略拒绝，仍在原处保留，但不再由新版或全局注册引用；不把此状态说成磁盘清理完成。正在运行的旧会话不会因磁盘配置更新自动换成新服务；重启／新会话后核对实际身份。不要为了清理而终止用户游戏进程、删除调查报告、恢复工程或存档。
