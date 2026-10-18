# Unity项目基础参考

本参考整理自用户提供的《Unity项目开发规范》。以下是默认基线；已有项目约定和明确架构决定优先。模板里的`<Studio>`、`<Project>`和模块名必须由当前项目确定，不能照抄示例。

## 目录与程序集

建议把自有内容收在`Assets/<OwnerOrProject>/`下，并按实际规模划分：

```text
Scripts/{Core,Gameplay,Presentation,UI,DataRuntime,Tools,Validation,Tests}
Art/{Audio,Sprites,Models,Animations,Materials,Shaders,VFX}
Prefabs/<Domain>
Scenes/{Main,Test}
Data/{Tables,ScriptableObjects,Generated}
Documentation/{Systems,Execute}
```

- 第三方包保持独立；适配器放自有目录。
- Editor代码进入Editor专用程序集；运行时程序集不能依赖Editor。
- 生成物集中到可删除、可重建的`Generated`。
- 一个文件一个主要public顶层类型；文件和类型使用英文PascalCase。
- `.meta`随资产移动和提交。
- 小项目可以合并目录和程序集，但仍保持职责和依赖方向。

常见asmdef方向：`Core ← Gameplay ← Presentation ← UI`，Audio／FX可依赖Core和各自框架，Editor／Tests依赖被编辑或被测程序集。根据项目裁剪，禁止循环。

## 场景组合

典型根对象包括Camera、Environment、World、GameSystems、Events、UI、Audio和FX。它们是职责提示，不要求所有项目使用固定名称或固定层级。

- 作者摆放对象的位置、旋转和缩放由场景保存；开局不无条件覆盖。
- 敌人、道具、子弹、临时特效等内容实例可动态生成。
- 依赖优先通过Inspector、Prefab、工厂或Composition Root显式提供。
- `Reset/OnValidate`只自动绑定本对象上唯一无歧义的组件；多个候选必须要求明确选择。
- 不在热路径使用`FindObjectOfType`、`GameObject.Find`或字符串查找。
- 不依赖Script Execution Order掩盖普通初始化依赖。

## 架构选择的优化

原规范中的“禁止Bootstrapper／静态事件／单例／跨场景常驻”调整为条件性规则：

- 场景型小项目默认手动装配，便于检查和调试。
- 多场景应用层确有共享服务时，可使用Composition Root或受控常驻对象，但必须定义创建唯一性、销毁、场景切换、Domain Reload、测试替换和退出清理。
- 静态事件只有在生命周期与Domain Reload安全、订阅清理可验证时才可采用；默认仍优先实例事件。
- 自动装配只能处理无歧义、可预览、可撤销的连接，不能覆盖作者Transform或静默选择候选。

## 重开基线

无需重载场景的游戏应验证至少三次连续重开。检查Director状态、领域状态机、生成实例、定时器、随机队列、Actor局部状态、相机、输入锁和UI暂存。若项目明确采用场景重载，仍需验证静态状态、常驻对象和异步任务不会泄漏。
