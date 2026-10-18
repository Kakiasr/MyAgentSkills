---
name: game-rendering-technical-art
description: "Design, implement, review, or debug game rendering solutions for shaders, materials, lighting, post-processing, VFX graphs, render features, transparency, and visual quality tiers. Route pipeline automation and performance diagnosis to their specialists."
---

# 游戏渲染技术美术

## 职责

把`VIS-*`转成Shader、材质、灯光、后处理、VFX图和渲染特性，拥有渲染实现与质量档位的视觉差异；不拥有资产导入流水线或性能诊断结论。

先读[美术专项交接契约](../../references/art-specialist-contract.md)。Unity任务按实际管线调用Shader Graph、URP或Render Graph专项技能。

## 工作流与交付

1. 确认引擎、渲染管线、色彩空间、平台、相机、透明／光照需求和不可牺牲视觉项。
2. 定义材质模型、Shader输入、灯光分层、后处理顺序、VFX接口和降级档位。
3. 实现或给出精确入口、参数、版本、依赖、限制和回滚方式。
4. 在代表场景验证外观、排序、深度、阴影、变体和跨质量档一致性。

输出`TA-*`实现记录、材质／Shader规范、质量档矩阵、验证截图或测量来源及未验证项。
