# 依赖说明

权威机器清单位于[`dependencies.json`](../dependencies.json)。依赖按用途分层；不要为使用一个技能安装所有可选分析引擎。

## 核心运行时

- Node.js：版本范围与REA 6.7.0保持一致，为`^22.19.0 || ^24.11.0 || >=26.0.0`。REA启动器、文档集校验、路由测试和JavaScript示例模型都使用Node标准库。
- `rea-agents@6.7.0`：仅`game-analysis`技术路线需要，由`scripts/rea/setup.mjs`安装到插件专属用户缓存；插件不打包`node_modules`。

## Python

- Python 3.10或更高版本：只在渲染／测试游戏循环图时需要。`render_loop.py`和对应测试只使用标准库。
- PyYAML `>=6.0,<7.0`：仅用于开发期运行`skill-creator/scripts/quick_validate.py`，记录在根目录`requirements-dev.txt`。它不是循环图渲染、REA或普通技能调用的运行时依赖。

开发者可在隔离环境中安装：

```sh
python -m pip install -r requirements-dev.txt
```

不要由技能隐式修改全局Python环境。

## 工程和宿主工具

- Unity：仅Unity项目执行、编辑器测试和构建需要，版本必须服从目标项目，而不是插件固定版本。
- Git：开发端同步、差异检查和迁移建议使用。
- Codex CLI：本地插件安装／重载需要支持`codex plugin`命令的版本。

## REA可选分析引擎

Ghidra/JDK、JADX/Java、IDA、Kuna、Binwalk/Unblob、tshark/capinfos、sigrok-cli、WABT和pwntools均为特定目标路线的外部依赖。只有当前调查需要对应能力时才检查和配置；REA连接成功不代表这些provider都可用。版本和环境变量要求以`game-analysis`随包上游参考与当前REA会话能力为准。

## 检查

```sh
node scripts/verify-dependencies.mjs
node scripts/verify-dependencies.mjs --dev
```

默认命令只把核心必需项缺失视为失败；`--dev`还要求Python和PyYAML可用。脚本只读取版本和导入状态，不安装或修改依赖。
