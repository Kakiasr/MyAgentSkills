---
name: game-animation-design
description: "Design or review gameplay animation language, motion timing, poses, locomotion sets, combat readability, transitions, anticipation, hit reactions, camera-relative readability, animation events, and production briefs."
---

# 游戏动画设计

## 职责

拥有动作语言、关键姿势、节奏、过渡、循环、受击和状态表现的设计意图与动画清单。玩法状态机是真值来源；本技能不实现Animator、骨骼或动画文件。

先读[美术专项交接契约](../../references/art-specialist-contract.md)。

## 工作流与交付

1. 映射`ACT/STA/EVT-*`到动画意图、启动／持续／恢复阶段和可取消窗口。
2. 定义轮廓、重心、预备、发力、跟随、节奏、镜头距离和敌我差异。
3. 建立动画集、过渡表、循环策略、根运动选择、事件帧需求和运动减弱替代。
4. 输出`VIS-*`动作规则、镜头参考、`AST-*`动画清单、时长来源、验收用例和待实现问题。

不得用动画事件决定核心伤害真值；事件帧只消费程序确认的时序契约。
