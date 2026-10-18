---
name: game-technical-art
description: "Use when bridging art and engineering through rendering design, shaders, materials, lighting, VFX implementation, asset import automation, validation tools, graphics debugging, memory and GPU budgets, batching, LOD, platform quality tiers, or visual performance optimization."
---

# Game Technical Art

## 职责

保证视觉目标能够在目标引擎、平台和性能预算内稳定实现。负责渲染与材质方案、Shader、灯光和 VFX 落地、资产管线、验证工具、性能测量与跨专业问题定位。

## 工作流

1. 确认目标引擎、渲染管线、平台、分辨率、目标帧率、质量档位和硬件下限。
2. 从美术设计提取必须保留的视觉特征，从程序架构提取渲染时序、数据来源和运行时约束。
3. 建立可测量预算：帧时间、draw call、三角形、骨骼、贴图内存、RenderTexture、粒子、透明层数、Shader 变体和加载峰值。
4. 设计材质、Shader、灯光、后处理、VFX、LOD、合批、实例化、Atlas 和流式加载方案。
5. 建立资产导入、命名、检查、自动修复和报告工具，减少依赖人工记忆的步骤。
6. 在代表性最差场景和目标设备上采样，再依据 profiler 或帧调试证据优化。

## 引擎路由

- Unity：按项目实际渲染管线调用 Shader Graph、URP、Sprite Atlas、音频或构建优化等匹配技能；先确认 Unity 版本和 Render Pipeline Asset。
- 其他引擎：先确认渲染后端、材质模型、资源导入器、性能分析器和目标设备，再提出实现。

## 技术美术规格

至少包含：

- 视觉目标与不可牺牲项。
- 平台、渲染路径和质量档位。
- 每类资产预算与场景总预算。
- Shader、材质、灯光、VFX 和后处理规则。
- 资产导入预设、验证规则和自动化入口。
- 性能采样场景、采样设备、指标与通过阈值。
- 降级顺序和各档位的视觉差异。
- 美术、程序与技术美术各自负责的问题。

## 诊断原则

- 先捕获问题发生的代表性帧或资源，再提出优化。
- 区分 CPU、GPU、内存、带宽、加载和构建体积问题。
- 优化前后使用相同场景、相机、设备和质量档位对比。
- 不用“减少面数”“合批”“降低贴图”作为无测量依据的通用答案。
- 不以破坏轮廓、状态识别或核心视觉反馈为默认代价。

## 完成条件

- 视觉目标在目标质量档位中可复现。
- 预算有明确单位、测量方法和阈值。
- 资产违规能被工具发现或由清晰检查表复现。
- 性能结论附带测量环境和优化前后数据。
- 降级方案已说明对视觉和玩法可读性的影响。

