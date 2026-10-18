# Kaki的游戏开发工具

这是一个全新的、独立的本地游戏开发插件，不继承旧插件的身份或结构。它覆盖五类专业能力：

1. 游戏设计：体验、玩法、循环、系统、关卡、经济与内容结构。
2. 游戏程序架构与开发：技术方案、模块边界、数据、运行时、工具、测试与实现。
3. 游戏美术设计：视觉目标、风格、角色、场景、界面、动画和特效设计。
4. 游戏美术资产创建：规格、生产、命名、版本、导出、验收与引擎交付。
5. 游戏技术美术：渲染、Shader、材质、性能、资产管线、自动化和视觉问题诊断。

统一入口负责识别需求、安排专业顺序、传递跨专业约束和组织验收。每个专业技能只对自己的职责作最终判断。

## 主要技能

- `game-development-workflow`：统一入口与跨专业编排。
- `game-design`：游戏设计。
- `game-programming-development`：游戏程序架构与开发。
- `game-art-design`：游戏美术设计。
- `game-art-asset-creation`：游戏美术资产创建。
- `game-technical-art`：游戏技术美术。

## 本地标识

- 插件 ID：`kaki-game-development-tools`
- 展示名称：`Kaki的游戏开发工具`
- 本地市场：`kakiasr-local`

## 0.4.0 知识引用更新

游戏设计技能现使用《游戏核心体验设计》200 页校注全文，替换原摘要。按“缺字明确标注、原文保留、勘误另列”组织，并随附原始文字层和 200 张原页图；24 张循环图与 24 张层次图按阅读顺序整理。原稿缺损不猜补，事实与公式不因收录而视为已验证。

- [全文](skills/game-design/references/core-experience-design.md)
- [勘误与补录](skills/game-design/references/core-experience-design-errata.md)
- [原始文字层](skills/game-design/references/core-experience-design-source.md)

资料仅作为用户提供的知识引用；插件代码的 MIT 许可不自动覆盖原资料版权。

## 跨电脑安装与同步（0.4.2）

分发仓库为 `https://github.com/Kakiasr/MyAgentSkills`，市场 ID 保持 `kakiasr-local`。需要 Git、Codex CLI，以及可访问 GitHub 的网络。以下命令适用于提供 `codex plugin` 命令的 Windows / macOS / Linux 环境；各电脑独立安装和登录 Codex，不同步凭据或整个 `.codex` 目录。

### 首次安装（使用端）

```sh
codex plugin marketplace add https://github.com/Kakiasr/MyAgentSkills.git --ref main
codex plugin add kaki-game-development-tools@kakiasr-local
```

若电脑已经配置同名的本地市场，先运行 `codex plugin marketplace list --json` 检查来源。不要直接删除或替换开发用本地市场；本地市场与 Git 市场同名时应选择其中一种工作方式。

### 获取已发布更新（使用端）

```sh
codex plugin marketplace upgrade kakiasr-local
codex plugin add kaki-game-development-tools@kakiasr-local
codex plugin list --json
```

第一步获取 Git 市场的新快照，第二步安装新版插件。每一步成功后再执行下一步；失败时停止并保留错误。确认安装版本后新建会话使用新版技能。以上为手动更新，不是后台自动同步，也不会上传此电脑的本地修改。

### 开发端发布

继续以仓库中的 `plugins/kaki-game-development-tools/` 为源文件；不要修改安装缓存。每次发布检查远端改动、完成校验、提高 `plugin.json` 的版本，并只提交本次插件相关文件。推送成功后，其他电脑执行上面的更新命令。

本地路径注册的市场不由 `marketplace upgrade` 拉取 Git；开发端需要先安全同步仓库，再执行 `codex plugin add kaki-game-development-tools@kakiasr-local`。有未提交修改或分叉时先处理，不使用强制覆盖。

### 外部技能依赖

本插件包含六个技能和核心体验全文资料，可以独立安装。若用户另外安装了 `gamedesign` 技能，游戏设计技能可按需结合其知识库和模板；本插件不依赖它。Unity、图像生成等工具需要各设备自行配置。

本仓库不会同步登录凭据、个人会话、其他插件缓存或本机工具安装。遇到 GitHub 访问或认证问题时先修复连接，不通过复制凭据解决。

## 推荐调用方式

- “把这些零散创意整理成一个可制作的核心玩法原型。”
- “为这个系统设计程序架构，并列出代码、数据和测试任务。”
- “为这个项目制定统一的美术风格、资产规范和技术美术预算。”

