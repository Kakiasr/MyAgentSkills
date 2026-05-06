# Unity Design Patterns Reference

This reference is derived from the user-provided `Design Pattern.docx`. Use it when producing game system specs or Unity implementation plans that should apply design patterns.

## Pattern Selection Table

| 类别 | 模式 | 关键词 | 典型 Unity 用途 | Use when |
| --- | --- | --- | --- | --- |
| 创建型 | 单例模式 Singleton | 全局唯一 | GameManager, AudioManager, UIManager, SaveManager | One service must have one authoritative runtime instance and global access is acceptable. |
| 创建型 | 工厂模式 Factory | 对象生成 | 武器、敌人、道具生成器 | Callers should request an object by type/id without knowing construction details. |
| 创建型 | 抽象工厂模式 Abstract Factory | 产品族 | 阵营、主题、关卡套装 | A theme/faction needs to create several related object types together. |
| 创建型 | 建造者模式 Builder | 分步组装 | NPC、装备、关卡构造 | A complex object is assembled through ordered steps and variations share the same build process. |
| 创建型 | 原型模式 Prototype | 克隆 | Prefab, 对象池初始对象 | New instances should clone an existing object or prefab. In Unity, `Instantiate(prefab)` is the common form. |
| 结构型 | 对象池模式 Object Pool | 复用 | 子弹、特效、浮字、敌人波次 | Objects are created and destroyed frequently and reuse reduces runtime allocation/spikes. |
| 结构型 | 外观模式 Facade | 统一接口 | GameFacade, match start/end orchestration | A single high-level operation must coordinate save, audio, UI, scene, rewards, or other subsystems. |
| 结构型 | 装饰器模式 Decorator | 动态扩展 | 附魔、buff、临时效果 | Behavior or effects are added dynamically without changing the base object class. |
| 结构型 | 适配器模式 Adapter | 接口兼容 | 新旧输入系统、第三方 SDK 包装 | Existing code must talk to an incompatible API through a stable project-facing interface. |
| 行为型 | 观察者模式 Observer | 事件通知 | UI 更新、任务系统、属性变化 | A subject's state change should notify direct subscribers. |
| 行为型 | 状态机模式 State | 行为切换 | 角色 AI、玩家动作、交互物状态 | An object has named modes and behavior changes per mode. |
| 行为型 | 策略模式 Strategy | 可替换算法 | 攻击模式、AI 策略、奖励计算 | Algorithms/policies must be swapped by data, difficulty, enemy type, or equipment. |
| 行为型 | 命令模式 Command | 可撤销命令 | 关卡编辑器、输入回放、行动队列 | Actions need to be stored, replayed, cancelled, undone, or serialized. |
| 行为型 | 订阅发布模式 Publish-Subscribe | 解耦通信 | 全局事件系统、跨系统消息 | Publishers and subscribers should not reference each other directly. |

## Common Game System Mapping

| 系统模块 | 推荐模式 |
| --- | --- |
| GameManager or boot flow | Singleton, Facade |
| Enemy generation | Factory, Prototype, Object Pool |
| Skill casting | Command, Strategy, Observer |
| AI logic | State, Strategy |
| UI refresh | Observer or Publish-Subscribe |
| Projectile/VFX reuse | Object Pool, Prototype |
| Multi-system coordination | Facade, Publish-Subscribe |
| Buff/enchant/modifier system | Decorator, Strategy |
| Input compatibility | Adapter, Command |

## Output Guidance

When adding design patterns to a system spec:

1. Name the implementation pressure first, such as object creation, object reuse, state switching, algorithm variation, undo, interface compatibility, or cross-system notification.
2. Recommend the smallest useful pattern set. One to three patterns is usually enough for a single system.
3. Attach each pattern to a concrete object or file, not only to the system as a whole.
4. State the tradeoff or risk, such as global coupling for Singleton, factory modification cost, event lifecycle leaks, or over-abstraction.
5. Include an acceptance check that proves the pattern works in the intended system.

Avoid:

- Adding Singleton to every manager by default.
- Using Factory when a direct prefab reference is enough.
- Using Observer or Publish-Subscribe without unsubscribe/lifecycle rules.
- Using State when the object only has a boolean flag and no behavior differences.
- Using Strategy for a one-off algorithm that is not expected to vary.
- Combining too many patterns before the system boundary is stable.
