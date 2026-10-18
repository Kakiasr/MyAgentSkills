---
name: game-2d-asset-production
description: "Plan, create, edit, export, organize, or validate game-ready 2D assets: concept paintovers, sprites, frame animation, tiles, textures, UI images, icons, atlases, pivots, slicing, transparency, and engine import packages."
---

# 游戏2D资产生产

## 职责

把批准的`VIS-*`转为可追踪的2D源文件与引擎资产，拥有尺寸、分层、色彩空间、透明边缘、pivot、切片、图集、导出和版本记录。视觉方向变化必须回交设计所有者。

先读[美术专项交接契约](../../references/art-specialist-contract.md)。序列帧和Sprite Sheet专项优先调用仓库`2d-game-animation-assets`；Unity切片、Atlas和UI导入调用匹配Unity技能。

## 工作流与交付

1. 确认用途、镜头占比、目标分辨率、像素密度、缩放、过滤、压缩和目标引擎。
2. 先制作代表资产并在引擎中验证，再批量生产。
3. 分离源文件、导出文件和引擎资产，使用稳定命名及版本。
4. 输出`AST-*`清单、来源授权、源／导出／引擎路径、尺寸、pivot、切片、帧率、导入设置和验收结果。

未做引擎验证时不得称为可直接使用的成品。
