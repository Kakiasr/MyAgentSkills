---
name: game-software-architecture
description: "Design or review engine-agnostic game software architecture: module boundaries, data ownership, commands, queries, events, lifecycle, persistence, networking boundaries, technical risks, and implementation sequencing. Do not use for focused coding or build validation."
---

# 游戏软件架构

## 职责

把已确认的游戏设计规则转换为技术边界和可实施顺序。负责模块职责、依赖方向、数据所有权、运行时生命周期、跨系统契约、持久化／联网边界、可复现性和架构风险；不以架构方案冒充已经实现。

输入使用`SYS/ACT/EVT/CFG/DAT/REQ/NFR/AC-*`。规则缺失时建立`Q-*`；架构取舍使用`DEC-*`并记录背景、选择、替代方案、影响和回滚条件。

## 工作流

1. 识别引擎、版本、平台、团队规模、内容规模、性能目标和现有工程约束。
2. 将需求拆成静态配置、运行时状态、命令、查询、事实事件、持久化数据和表现反馈。
3. 为每份可变数据指定唯一所有者，列出读者、写者、生命周期和恢复策略。
4. 划定模块和依赖方向；优先窄接口，禁止用全局访问便利性掩盖所有权不清。
5. 明确初始化、更新、暂停、结束、重开、卸载和异常恢复顺序。
6. 处理随机种子、时间单位、帧率依赖、序列化版本、线程／异步和联网权威边界。
7. 给出最小垂直切片、风险探针、迁移顺序和架构验收，不提前设计未被需求证明的框架。

## 默认原则与可记录例外

- 配置、运行时状态、模拟、表现和编辑器工具分离。
- 命令用于请求改变，查询同步读取状态，事件只描述已经发生的事实。
- UI、Audio、FX不反向拥有玩法真值。
- 核心规则不依赖帧率；时间源和更新阶段必须明确。
- 随机性可注入种子，关键模拟可复现。
- 单例、静态事件、服务定位、自动装配、跨场景常驻并非绝对禁止；只有需求和生命周期证明其必要时采用，并记录所有权、清理、测试和回滚条件。

Unity架构任务若涉及目录、程序集、场景组合或重开基线，交给`unity-project-foundation`细化。具体功能代码交给`gameplay-programming`，验证交给`game-testing-and-validation`。

## 交付

- 模块／对象职责和排除范围。
- 数据所有权、命令／查询／事件契约。
- 生命周期和关键时序。
- 架构决定记录及替代方案。
- 文件／程序集／资产映射建议。
- 风险、实现顺序和可观察验收。
