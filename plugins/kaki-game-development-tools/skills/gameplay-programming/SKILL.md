---
name: gameplay-programming
description: "Implement, extend, review, or debug gameplay code and runtime systems from confirmed design rules. Use for actors, domain systems, state machines, input, time, spawning, inventory, save logic, AI, and runtime defects; route project scaffolding, editor tooling, and independent validation elsewhere."
---

# 游戏玩法程序开发

## 职责

在现有工程中实现、评审或调试明确的玩法规则和运行时系统。尊重既有架构与用户改动，不把实现任务扩展成无关重构；用户只要求诊断时不修改代码。

Unity任务开始前读取[Unity运行时实现基线](references/unity-runtime-baseline.md)。若当前环境提供匹配的`unity-workbench`或`unity`专项技能，按其规则执行实际工程操作。

## 工作模式

- **实现**：完成一条可运行的需求路径及必要测试。
- **扩展**：在已有系统边界内增加功能，保持序列化与存档兼容。
- **评审**：按规则ID、所有权、生命周期和异常路径给出问题，不自动改动。
- **调试**：复现→缩小范围→确定原因→给出证据；获得修复任务后才实施并回归。

## 工作流

1. 读取项目规范、引擎版本、包、相关代码、场景／Prefab、测试和用户未提交改动。
2. 将需求映射为拥有者、配置、运行时数据、状态、命令、查询、事件及失败语义。
3. 先走通最小正常路径，再补失败、重复调用、中断、暂停、重开和存档恢复。
4. Unity中保持`Awake`、`OnEnable`、`Start`、`Update/FixedUpdate`、`OnDisable/OnDestroy`职责明确；同一模拟不能被两个更新入口重复驱动。
5. 事件订阅必须对称解绑；事件载荷只包含订阅者所需数据，高频路径避免反射、装箱和临时集合。
6. 运行状态不得写回共享配置资产；序列化字段变更考虑旧场景、Prefab和存档迁移。
7. 运行最小相关测试并报告实际执行环境。独立的完整测试／构建审查交给`game-testing-and-validation`。

## 代码质量边界

- 类和方法按实际复杂度写注释；公共契约及非显然约束必须说明，简单私有方法不强制机械重复XML注释。
- 默认私有字段和意图API；只有真实扩展点才允许继承。
- 状态机有明确初态、合法转移、非法转移处理和进入／退出副作用；简单二态对象不强行模式化。
- 缺失依赖给出对象与字段上下文，不吞掉无法恢复的异常。
- 不使用字符串查找或每帧全局搜索作为正式依赖方案。

## 完成条件

- 修改可追溯到设计／需求ID，文件职责清晰。
- 正常、失败、重复、中断和重开语义有实现或明确不适用。
- 编译、相关测试和必要场景连接已验证；未执行项明确列出。
- 没有把未经确认的玩法决定藏在代码默认值中。
