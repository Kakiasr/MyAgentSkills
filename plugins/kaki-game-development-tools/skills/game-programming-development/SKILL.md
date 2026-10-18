---
name: game-programming-development
description: "Compatibility router for game programming requests that span architecture, gameplay implementation, Unity project foundations, Unity data/editor tooling, or testing and validation. Route focused work to the matching specialist instead of handling every programming concern here."
---

# 游戏程序开发路由

## 职责

保留原调用ID，识别程序开发请求属于哪个专项技能，并组织必要交接。本技能不再直接承担全部架构、实现、工具、调试和测试工作。

输入优先采用`game-system-design`的系统规则、配置、行为和验收ID。发现玩法规则、费用、目标、次数或结算点未定时，建立`Q-*`并回交设计，不用代码默认值替代设计决定。现有发行游戏的事实还原交给`game-analysis`。

先读[插件级路由与交接契约](../../references/skill-routing-and-handoff.md)。仅在请求跨越两个以上程序专项、用户显式调用旧ID，或需要规划端到端程序交付时使用本路由器；单项请求直接进入专项技能。

## 专项路由

| 用户目标 | 主责技能 | 不属于该技能的内容 |
| --- | --- | --- |
| 技术方案、模块边界、数据所有权、接口、生命周期、存档／联网边界 | `game-software-architecture` | 不默认改代码 |
| 实现、扩展、评审或调试玩法代码和运行时系统 | `gameplay-programming` | 不重新定义产品规则 |
| Unity目录、asmdef、场景组合、依赖装配、启动／重开生命周期 | `unity-project-foundation` | 不实现具体玩法算法 |
| Unity配置资产、Prefab、序列化、Inspector、Editor工具和内容校验器 | `unity-data-and-editor-tooling` | 不拥有本局运行状态 |
| 测试策略、复现、EditMode／PlayMode、构建冒烟和交付验证 | `game-testing-and-validation` | 不在只要求验证时顺带修复 |

Unity功能实现通常以`gameplay-programming`为主；只有任务实际涉及工程基础、内容工具或验证时，才再调用对应Unity专项。若环境中存在更细的`unity-workbench`或`unity`技能，按其触发范围执行具体Unity操作，本插件专项继续拥有架构基线、交接和验收口径。

## 编排顺序

1. 记录工程、引擎版本、平台、输入规则ID、范围和明确排除项。
2. 选择一个主责技能；其余技能只接收明确的交接问题，不把一次小改动升级成全面重构。
3. 架构未定且会影响实现时：`game-software-architecture` → 实现专项。
4. Unity新项目或工程骨架不可靠时：`unity-project-foundation` → `gameplay-programming`。
5. 配置、Prefab或策划编辑入口是需求的一部分时：实现专项 → `unity-data-and-editor-tooling`。
6. 代码或资产变更完成后：`game-testing-and-validation`按风险验证；失败证据回交实际所有者。
7. 汇总设计ID→架构决定→文件／资产→测试证据，不重复维护各专项正文。

## 完成条件

- 每项工作只有一个主责技能，跨技能输入和输出明确。
- 旧`game-programming-development`调用被正确路由，没有以总入口代替专项判断。
- 已确认、假设、架构决定、实现状态和验证状态没有混写。
- 未执行的Unity编辑器步骤、构建和手工检查均明确列出。
