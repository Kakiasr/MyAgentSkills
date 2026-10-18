---
name: game-art-pipeline
description: "Design, implement, review, or repair art asset pipelines: folder and naming conventions, DCC export, engine import presets, metadata, dependency tracking, validation, batch processing, automated fixes, build-time checks, and production reports."
---

# 游戏美术资产管线

## 职责

拥有从DCC源文件到引擎资产的路径、命名、元数据、导入预设、依赖、校验、批处理、自动修复和报告。它执行批准规格，不重新定义视觉或玩法。

先读[美术专项交接契约](../../references/art-specialist-contract.md)。Unity ScriptedImporter、AssetPostprocessor、Editor工具和内容校验可交给`unity-data-and-editor-tooling`实施。

## 工作流与交付

1. 盘点资产类别、源格式、DCC、导出器、引擎版本、目录和现有失败模式。
2. 定义稳定ID、命名、版本、源／导出／引擎边界、依赖和迁移策略。
3. 将可机械判断的规则实现为检查器；自动修复必须可预览、可回滚且不破坏源文件。
4. 用合格、失败、边界和旧资产样本验证导入、报告与构建门。

输出`TA-*`管线契约、工具入口、规则清单、报告格式、迁移计划、测试样本和失败恢复方式。
