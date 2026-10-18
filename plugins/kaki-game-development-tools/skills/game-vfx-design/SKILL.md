---
name: game-vfx-design
description: "Design or review gameplay VFX language, effect hierarchy, timing, color and shape encoding, hit and ability feedback, environmental effects, screen-space effects, accessibility, and VFX production briefs."
---

# 游戏VFX设计

## 职责

拥有玩法特效的视觉语言、信息层级、形状／色彩／节奏编码、生命周期和生产简报。伤害、碰撞和状态由玩法系统拥有；Shader与粒子实现交给渲染技术美术。

先读[美术专项交接契约](../../references/art-specialist-contract.md)。

## 工作流与交付

1. 将技能、命中、范围、危险、增益、减益和环境状态映射到`EVT-*`。
2. 定义预警、发生、命中、持续、结束各阶段的形状、明度、色彩、空间和时长。
3. 建立同屏优先级、遮挡、透明叠层、闪烁、运动减弱和色觉冗余规则。
4. 输出效果`VIS-*`、时序表、`AST-*`源素材需求、实现问题、预算输入和代表场景验收。

不能用效果缺失或延迟改变玩法结果；屏幕效果必须保留HUD和危险信息可读性。
