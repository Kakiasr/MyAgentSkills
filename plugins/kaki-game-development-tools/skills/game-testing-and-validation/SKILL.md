---
name: game-testing-and-validation
description: "Plan, implement, run, or review game testing and delivery validation across rules, state transitions, scenes, assets, serialization, performance boundaries, and builds. Use for evidence-backed readiness decisions; do not silently implement unrelated fixes."
---

# 游戏测试与交付验证

## 职责

把设计需求、架构决定和实现改动转换为可执行验证，并基于证据判断当前范围是否通过。用户只要求检查时保持只读；发现问题后给出最小复现、影响和归属，未经要求不顺带修复。

Unity项目读取[Unity验证矩阵](references/unity-validation-matrix.md)，并按环境调用匹配的`unity-workbench:unity-build-validation`、`unity-workbench:unity-bug-investigation`或其他Unity专项能力。

## 工作模式

- **测试设计**：从`REQ/ACT/STA/CFG/NFR/AC-*`建立覆盖矩阵。
- **自动化实现**：编写规则、EditMode、PlayMode、集成或冒烟测试。
- **缺陷验证**：复现、隔离、回归并记录环境和证据。
- **交付门禁**：检查编译、引用、序列化、内容、平台构建和已声明性能阈值。

## 工作流

1. 锁定版本、提交／工作区状态、Unity／引擎版本、平台、场景、测试范围和禁止改动。
2. 为每条关键需求覆盖正常、失败、边界、重复、中断、重开和恢复；按风险选择层级。
3. 先执行廉价确定性检查，再进行场景、PlayMode、构建和手工体验验证。
4. 区分“未执行”“无法执行”“失败”“通过”和“观察到但无阈值”；日志存在不等于测试通过。
5. 缺陷记录最小复现、期望、实际、证据、首次失败层级、可能所有者和回归用例。
6. 只有所有必需门禁通过且阻塞项为零时才称目标范围可交付。

## 完成条件

- 每个关键需求至少有一个验收或明确的未覆盖原因。
- 测试结果包含环境、命令／操作、退出状态和证据位置。
- 自动与手工验证、编辑器与构建、功能与性能分别报告。
- 不把“编译通过”当成场景连接、资源完整、重开或玩家体验已经验证。
