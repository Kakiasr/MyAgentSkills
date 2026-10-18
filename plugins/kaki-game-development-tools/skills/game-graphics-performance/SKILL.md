---
name: game-graphics-performance
description: "Measure, diagnose, optimize, or validate game graphics performance across GPU and render-thread time, draw calls, overdraw, geometry, texture and render-target memory, shader variants, particles, streaming, loading peaks, quality tiers, and device budgets."
---

# 游戏图形性能

## 职责

拥有图形预算、采样设计、瓶颈证据、优化实验和质量档验证。没有相同环境的测量时只能给候选假设，不能宣称已定位或已优化。

先读[美术专项交接契约](../../references/art-specialist-contract.md)。

## 工作流与交付

1. 固定设备、分辨率、质量档、相机、场景、帧区间和目标帧率。
2. 建立GPU／Render Thread、draw call、overdraw、几何、骨骼、纹理／RT内存、粒子、变体、加载峰值等`NFR-*`预算。
3. 捕获代表性最差帧，区分CPU提交、GPU、内存、带宽、加载和构建体积。
4. 每次只验证一个主要假设；优化前后使用相同环境并记录视觉／可读性影响。
5. 降级涉及视觉支柱时回交对应设计专项批准。

输出采样环境、工具证据、指标表、瓶颈结论、实验结果、质量档差异和仍待验证项。
