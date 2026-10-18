---
name: unity-project-foundation
description: "Create, review, or repair a Unity project's structural foundation: folders, assembly definitions, namespaces, scene composition, explicit dependency wiring, lifecycle ownership, reset semantics, and third-party boundaries. Do not use for implementing a focused gameplay feature."
---

# Unity项目基础架构

## 职责

建立或审查Unity工程的可读结构和可验证装配，使目录、程序集、场景层级和生命周期能够说明对象职责。具体玩法实现交给`gameplay-programming`；配置Inspector和编辑器工具交给`unity-data-and-editor-tooling`；测试与构建判定交给`game-testing-and-validation`。

每次读取[项目基础参考](references/project-foundation.md)。现有工程以兼容和增量迁移为先，不为符合模板而批量移动资产或重写架构；移动Unity资产必须保留`.meta`和引用。

## 工作流

1. 确认Unity版本、渲染管线、目标平台、仓库状态、现有目录、asmdef、场景和第三方包边界。
2. 识别Composition Root、Director、领域系统、Actor、Events、UI、Audio、FX、配置和Editor工具的实际所有者。
3. 建立允许的程序集依赖图并检查循环；目录和命名空间服务于边界，不因项目很小而过度拆分。
4. 设计或修复场景组合：核心对象可检查、依赖可验证、动态内容与作者摆放内容边界明确。
5. 明确加载、初始化、开始、暂停、结束、重开和卸载顺序。
6. 对单例、静态事件、Bootstrapper、`DontDestroyOnLoad`、服务定位等选择做情境判断；采用时记录生命周期和测试策略。
7. 给出迁移步骤、影响资产、验证办法和回滚点；未经用户授权不进行大规模目录迁移。

## 完成条件

- 目录、asmdef、命名空间和场景职责相互一致，无循环程序集依赖。
- 核心依赖在场景、Prefab或明确Composition Root中可检查，不依赖热路径搜索。
- 初始化和重开可重复；运行时状态不污染作者配置。
- 第三方包不被直接修改，适配代码位于自有边界。
- 已执行和未执行的场景、序列化与构建验证分别列出。
