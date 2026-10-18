# 第三方来源与定制边界

REA来自官方[rea-agents npm发布](https://www.npmjs.com/package/rea-agents)及[morluto/rea](https://github.com/morluto/rea)。本插件0.7.0使用2026-10-18查得的稳定版6.7.0；来源、tarball完整性和匹配技能版本见`scripts/rea/release.json`。

发布包的`skills/reverse-engineer-anything/SKILL.md`与六个参考文档原样保存在`skills/game-analysis/references/upstream-rea/`。0.8.0进一步将完整技术正文直接整合进`game-analysis/SKILL.md`，适配标题、引用路径与自建会话清理边界，并加入中文游戏优先入口；不注册第二个技能。版权与MIT许可见[rea-MIT.txt](licenses/rea-MIT.txt)。上游工具数、覆盖与系统前提以实际运行时为准。

`game-analysis`是面向用户小型独立游戏需求传递目标的定制层：机制／内容逐条核查、字段化行为、覆盖与冲突账本、系统树与循环图交接。定制不改变REA分析引擎，不代表上游官方游戏专项版本，不凭空增加游戏容器支持。

`scripts/rea/`是本插件的专属运行时安装、启动与分层验证入口，不再依赖REA Local或旧全局注册。运行时依赖在用户缓存安装；不分发node_modules、用户配置、凭据、游戏资源或恢复源码。上游参考中的全局安装方式不是本插件的默认配置方式。

核心体验资料版权说明仍以README为准；插件代码MIT不等于原稿或被分析游戏资源可以自由复制与分发。
