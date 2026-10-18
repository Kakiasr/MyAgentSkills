# Kaki的游戏开发工具

这是一个独立的本地游戏开发插件。完整整合REA 6.7.0技能并改写为游戏拆解入口，同时将程序和美术拆为可独立路由的专项能力：

1. 游戏体验与玩法设计：玩家感受、操作、决策、约束、反馈与原型假设。
2. 游戏系统设计：零散规则转系统树、已有树增量转写、配置与行为契约、例外与验收。
3. 游戏循环设计：行动、成本、反馈、结果、返回与退出，绘制可编辑循环图。
4. 游戏程序开发：兼容总路由、软件架构、玩法实现、Unity项目基础、Unity数据与编辑器工具、测试与交付验证。
5. 游戏美术设计：美术指导、角色道具、环境、UI视觉、动画和VFX分别负责自己的视觉规则。
6. 游戏美术资产生产：2D与3D资产分别负责规格、生产、版本、导出和引擎交付。
7. 游戏技术美术：渲染实现、资产管线和图形性能分别负责方案、工具与测量证据。
8. 游戏拆解：试玩／录像／规则／源码／授权发行包分析，将机制、数值、内容与证据交接给系统树及循环图。

统一入口负责识别需求、安排专业顺序、传递跨专业约束和组织验收。游戏设计文档技能负责将专业产物装配为面向复刻的可追溯文档集。每个专业技能只对自己的职责作最终判断。

## 主要技能

- `game-development-workflow`：统一入口与跨专业编排。
- `game-design-document`：整理创意并编排其他专业技能，输出面向复刻的可追溯游戏设计文档集。
- `game-analysis`：游戏拆解，面向游戏的REA适配版，同时支持不依赖REA的观察与规则分析。
- `game-design`：游戏体验与玩法设计，保留原调用ID，显示名已更名。
- `game-system-design`：游戏系统设计。
- `game-loop-design`：游戏循环设计。
- `game-programming-development`：程序开发兼容路由与跨专项编排。
- `game-software-architecture`：模块边界、数据所有权、接口、生命周期和技术决定。
- `gameplay-programming`：玩法代码与运行时系统实现、评审和调试。
- `unity-project-foundation`：Unity目录、asmdef、场景装配、依赖和重开基础。
- `unity-data-and-editor-tooling`：Unity配置、Prefab、序列化、Inspector和Editor工具。
- `game-testing-and-validation`：规则、状态、场景、资源、构建和交付验证。
- `game-art-direction`：全项目视觉支柱、风格边界与美术圣经。
- `game-character-and-prop-design`、`game-environment-art-design`、`game-ui-visual-design`：角色道具、环境和UI视觉设计。
- `game-animation-design`、`game-vfx-design`：动画与玩法特效设计。
- `game-2d-asset-production`、`game-3d-asset-production`：2D与3D游戏资产生产。
- `game-rendering-technical-art`、`game-art-pipeline`、`game-graphics-performance`：渲染实现、资产管线和图形性能。

## 路由与文档一致性

- `game-development-workflow`负责推进规划、制作、集成、调试和验收；`game-design-document`负责创建、更新、迁移与校验正式文档集。
- 对一款完整游戏提出未限范围的“拆解一次／完整拆解／复刻／还原”时，默认进入`game-design-document`；`game-analysis`只负责其中的证据阶段。只有单一机制问题或明确要求概览／证据报告时，才在`game-analysis`收口。
- 公共ID、权威所有权、最小交接包和变更传播规则见[插件级路由与交接契约](references/skill-routing-and-handoff.md)。
- 正式文档集采用“一系统一文档”：`04-system-index.md`只维护关系，每个系统的规则正文位于`systems/<SYS-ID>-<slug>.md`。
- 文档集使用`document-set.json`登记文件与跨文档引用，运行以下命令检查缺失文件、重复／失效ID、系统归属、需求验收和配置消费者：

```sh
node skills/game-design-document/scripts/validate_document_set.mjs <文档集目录>
```

校验通过只表示结构与引用一致，不代表规则正确、代码完成或玩家验证通过。

## 0.9.0 程序开发能力拆分

原`game-programming-development`保留为兼容路由器，程序结论分别由五个专项技能负责。用户提供的《Unity项目开发规范》被拆为渐进加载的Unity运行时、项目基础、数据工具和验证参考；不把整份长规范强制加载到每个程序任务。

规范中的项目偏好经过条件化处理：显式装配、实例事件和无场景重载重开仍是默认基线，但单例、Bootstrapper、静态事件、跨场景常驻不再无条件禁止；有明确需求时可以采用，必须记录生命周期、清理、测试和回滚。机械性的“每个private方法必须写XML注释”改为公共契约与非显然约束必须说明，避免低信息注释。

## 0.10.0 美术能力直接重构

移除原`game-art-design`、`game-art-asset-creation`和`game-technical-art`三个过宽入口，不保留兼容路由。美术职责直接拆为11个可独立调用的专项技能，共享[美术专项交接契约](references/art-specialist-contract.md)，分别拥有`VIS-*`、`AST-*`、`TA-*`和`NFR-*`权威产物。

## 本地标识

- 插件 ID：`kaki-game-development-tools`
- 展示名称：`Kaki的游戏开发工具`
- 本地市场：`kakiasr-local`

## 依赖

- 机器可读清单：[`dependencies.json`](dependencies.json)
- 完整分层说明：[`references/dependencies.md`](references/dependencies.md)
- Python开发校验依赖：[`requirements-dev.txt`](requirements-dev.txt)，包含`PyYAML>=6.0,<7.0`
- 只读检查：`node scripts/verify-dependencies.mjs`；开发环境使用`--dev`

Node.js是插件脚本和REA入口的核心运行时；Python只用于循环图工具，PyYAML只用于技能开发校验。Ghidra、JDK、JADX、IDA、Kuna、Wireshark、sigrok、WABT、pwntools等按实际分析路线选装，不是普通用户的全量前置条件。

## 0.8.0 完整REA游戏定制版

[游戏拆解SKILL.md](skills/game-analysis/SKILL.md)现在直接包含完整REA技术执行正文，而非只摘取部分流程或把原技能作为可选参考。官方运行时全部工具与命令不做过滤，六个上游参考完整保留，额外增加中文游戏优先工作流、逐条规则表、例外与覆盖账本、系统树／循环图交接。[完整性与定制映射](skills/game-analysis/references/rea-customization.md)说明保留范围和升级校核。

完整集成指工作流、参考与工具集合保留，不代表所有外部引擎已安装、所有格式都支持或全部功能均已测试。各电脑依赖状态仍须分别验证。

## 0.7.0 游戏拆解与REA重部署

0.7.1增加本机`.cache/kaki-game-development-tools/rea/engines.json`配置，仅给REA子进程设置Ghidra目录与JDK目录；不覆盖系统Java或写死开发机路径。具体格式见运行说明。引擎、JDK和游戏恢复文件始终留在分发包外。

- [游戏拆解技能](skills/game-analysis/SKILL.md)：按问题选择观察、规则、源码或发行包路线，不把每次拆解变成全量逆向。
- [拆解模板](skills/game-analysis/templates/game-analysis-template.md)：版本身份、覆盖矩阵、字段化行为、冲突、验证及开发交接。
- [合成示例](skills/game-analysis/examples/chest-analysis.md)：展示如何保留结算顺序与未知项，不冒充真实商业游戏分析。
- `mcp.json`及`scripts/rea/`：单一`game-rea`服务，固定运行时`rea-agents@6.7.0`，仅使用`.cache/kaki-game-development-tools/rea/6.7.0`专属用户缓存。来源与完整性见`scripts/rea/release.json`。
- [随包上游技能及参考](skills/game-analysis/references/upstream-rea/SKILL.md)：来自6.7.0官方发布，与定制游戏拆解分层维护，不额外注册通用技能。
- [运行与迁移说明](skills/game-analysis/references/rea-runtime.md)、[第三方来源](THIRD_PARTY_NOTICES.md)。不打包游戏文件、恢复工程、node_modules或用户凭据。

本插件不再要求安装独立REA插件才能进行技术分析；首次换电脑仍需准备Node与REA运行时。无REA时可使用观察／规则／源码拆解，其余八个技能不以REA工具连接为前提。启动器不会隐式安装；经用户授权后可在插件根目录执行`node scripts/rea/setup.mjs`，npm不在PATH时传`--npm-cli`绝对路径。安装器只准备运行时，不注册市场、不替换技能、不安装分析引擎；首次下载需要网络，传递依赖由npm解析。

分层验证：`node scripts/rea/verify.mjs`检查握手、版本身份及provider状态；`node scripts/rea/verify.mjs --analysis`进一步对随包合成开箱样本做真实静态分析；附加`--output-dir`新建绝对目录保存报告。均不启动游戏。连接通过不代表原生反编译可用；特定引擎容器与加密格式需要各自支持，REA不是通用游戏解包器。

本次按用户授权移除旧REA Local插件、旧全局REA入口及旧依赖引用；旧插件源码和配置已在插件外备份。旧磁盘目录隔离操作被执行策略拒绝，暂保留原处且不再被新版引用，不将其称作磁盘清理完成。新版不读取旧缓存，不重复注册全局REA。宿主重启／新会话后才能确认实际切到新版；正在运行的旧会话不会自动替换，也不因本地插件安装而使移动端获得本机文件访问能力。

## 0.5.0 系统树与循环图

- [系统树模板](skills/game-system-design/templates/system-tree-template.md)：树表达关系与流程，表表达配置和行为，验收与证据分开。
- [增量更新约定](skills/game-system-design/references/incremental-update.md)：保留原图例、ID与无关已确认内容，输出变更、追溯和待决策项。
- [完整小型游戏示例](skills/game-system-design/examples/five-step-chests.md)：原创设计草案及数值模型，不含恢复工程或商业游戏资源。
- [循环图示例](skills/game-loop-design/examples/five-step-loop.md)：与系统树同一规则基线，另提供JSON布局。
- 循环渲染器`skills/game-loop-design/scripts/render_loop.py`只用Python标准库，输出SVG、Mermaid和结构检查；未预览时不声称已完成视觉验收。

原`game-design`的内部名称、引用资料和调用保持兼容；现在只负责体验与玩法，不再独占系统树和正式循环图。纯转写需求不强制先重做体验策划，纯循环图需求不默认实现游戏。

## 0.4.0 知识引用更新

游戏设计技能现使用《游戏核心体验设计》200 页校注全文，替换原摘要。按“缺字明确标注、原文保留、勘误另列”组织，并随附原始文字层和 200 张原页图；24 张循环图与 24 张层次图按阅读顺序整理。原稿缺损不猜补，事实与公式不因收录而视为已验证。

- [全文](skills/game-design/references/core-experience-design.md)
- [勘误与补录](skills/game-design/references/core-experience-design-errata.md)
- [原始文字层](skills/game-design/references/core-experience-design-source.md)

资料仅作为用户提供的知识引用；插件代码的 MIT 许可不自动覆盖原资料版权。

## 跨电脑安装与同步（0.4.2）

分发仓库为 `https://github.com/Kakiasr/MyAgentSkills`，市场 ID 保持 `kakiasr-local`。需要 Git、Codex CLI，以及可访问 GitHub 的网络。以下命令适用于提供 `codex plugin` 命令的 Windows / macOS / Linux 环境；各电脑独立安装和登录 Codex，不同步凭据或整个 `.codex` 目录。

### 首次安装（使用端）

```sh
codex plugin marketplace add https://github.com/Kakiasr/MyAgentSkills.git --ref main
codex plugin add kaki-game-development-tools@kakiasr-local
```

若电脑已经配置同名的本地市场，先运行 `codex plugin marketplace list --json` 检查来源。不要直接删除或替换开发用本地市场；本地市场与 Git 市场同名时应选择其中一种工作方式。

### 获取已发布更新（使用端）

```sh
codex plugin marketplace upgrade kakiasr-local
codex plugin add kaki-game-development-tools@kakiasr-local
codex plugin list --json
```

第一步获取 Git 市场的新快照，第二步安装新版插件。每一步成功后再执行下一步；失败时停止并保留错误。确认安装版本后新建会话使用新版技能。以上为手动更新，不是后台自动同步，也不会上传此电脑的本地修改。

### 开发端发布

继续以仓库中的 `plugins/kaki-game-development-tools/` 为源文件；不要修改安装缓存。每次发布检查远端改动、完成校验、提高 `plugin.json` 的版本，并只提交本次插件相关文件。推送成功后，其他电脑执行上面的更新命令。

本地路径注册的市场不由 `marketplace upgrade` 拉取 Git；开发端需要先安全同步仓库，再执行 `codex plugin add kaki-game-development-tools@kakiasr-local`。有未提交修改或分叉时先处理，不使用强制覆盖。

### 外部技能依赖

本插件包含十五个技能、游戏设计文档集模板、系统树模板与示例、循环图渲染器、游戏拆解模板、REA启动入口和核心体验全文资料，可以独立安装。若用户另外安装了`gamedesign`技能，体验与玩法技能可按需结合其知识库；本插件不依赖它。绘图可直接交付Mermaid；随附SVG渲染器需要Python，示例数值模型需要Node.js，均不是读取／使用系统树技能的必装依赖。REA技术工具需要Node及已准备的REA运行时，外部分析引擎按具体任务配置；Unity、图像生成等工具需要各设备自行配置。

本仓库不会同步登录凭据、个人会话、其他插件缓存或本机工具安装。遇到 GitHub 访问或认证问题时先修复连接，不通过复制凭据解决。

## 推荐调用方式

- “使用 $kaki-game-development-tools:game-design-document，把我的创意和原作资料整理成可直接用于复刻的游戏设计文档集，未知项不要自行补全。”
- “把这些零散创意整理成一个可制作的核心玩法原型。”
- “使用 $kaki-game-development-tools:game-analysis，拆解我指定的游戏，先列证据与覆盖范围，再把已确认规则交接到系统树；不要把未知写成默认规则。”
- “完整拆解这个游戏”或“使用这个插件拆解一次这款游戏”默认创建游戏设计文档集，而不是只返回一篇静态分析摘要。
- “使用 $kaki-game-development-tools:game-system-design，把这些规则补进我已有的系统树，保留原ID并列出变更。”
- “使用 $kaki-game-development-tools:game-loop-design，根据这份系统树绘制循环图，不增加未确认的成长机制。”
- “为这个系统设计程序架构，并列出代码、数据和测试任务。”
- “使用 $game-software-architecture，为这些系统规则定义模块、数据所有权和生命周期。”
- “使用 $gameplay-programming，在现有工程里实现并调试这项玩法。”
- “使用 $unity-project-foundation，建立Unity工程目录、程序集和场景装配基线。”
- “使用 $unity-data-and-editor-tooling，制作配置资产、中文Inspector和校验器。”
- “使用 $game-testing-and-validation，建立覆盖矩阵并验证构建是否可交付。”
- “为这个项目制定统一的美术风格、资产规范和技术美术预算。”

