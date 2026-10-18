# Kaki的游戏开发工具

本仓库提供 Codex 插件 `kaki-game-development-tools`。六个技能覆盖游戏设计、程序架构与开发、美术设计、资产创建、技术美术和跨专业工作流。详情见[插件说明](plugins/kaki-game-development-tools/README.md)。

## 首次安装

```sh
codex plugin marketplace add https://github.com/Kakiasr/MyAgentSkills.git --ref main
codex plugin add kaki-game-development-tools@kakiasr-local
```

## 获取新版

```sh
codex plugin marketplace upgrade kakiasr-local
codex plugin add kaki-game-development-tools@kakiasr-local
```

每台电脑分别执行，版本由 `plugins/kaki-game-development-tools/plugin.json` 控制。已有同名本地市场的电脑先用 `codex plugin marketplace list --json` 检查来源，再决定使用本地开发市场或此 Git 市场。

旧仓库的自动同步脚本与定时任务不属于这个插件。若其他电脑仍运行旧仓库的自动提交或推送任务，请先停用，避免旧内容重新上传。

游戏核心体验知识引用由用户提供，包含校注全文及 200 张原页图。仓库公开可见；插件的 MIT 许可不自动改变原资料的授权。
