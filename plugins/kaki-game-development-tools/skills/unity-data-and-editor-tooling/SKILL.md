---
name: unity-data-and-editor-tooling
description: "Design, implement, review, or validate Unity data authoring and editor workflows: ScriptableObjects, Prefabs, serialized fields, custom Inspectors, property drawers, import tools, configuration tables, migrations, and authoring-time validators."
---

# Unity数据与编辑器工具

## 职责

让策划、美术和关卡人员能够安全创建、编辑、迁移和校验内容。负责配置资产、Prefab定义、序列化契约、Inspector体验、批处理／导入工具和编辑期校验；不把运行时状态写入共享资产，也不替代玩法系统拥有业务规则。

每次读取[数据与编辑器工具参考](references/data-and-editor-tooling.md)。若请求仅是使用已有Unity编辑器完成具体资产操作，同时存在更精确的`unity`专项技能，按其规则执行实际操作。

## 工作流

1. 明确使用者、内容粒度、权威来源、生命周期、版本和运行时消费者。
2. 在Prefab、ScriptableObject、外部表和运行时模型间选择所有权，不用单一载体解决全部数据。
3. 定义字段类型、单位、默认值、范围、枚举、必填、依赖条件、迁移和失败提示。
4. 设计Inspector、PropertyDrawer、EditorWindow或导入流程，保留Undo、多对象编辑、Prefab Override和序列化兼容。
5. 为缺失引用、重复ID、断链、空池、非法范围和不支持的绑定建立编辑期验证。
6. 对批量写入先提供预览／dry-run，限定目标并保留可恢复性；不修改第三方源文件。
7. 用至少一个有效、一个无效和一个迁移样本验证工具。

## 完成条件

- 配置、定义和运行时状态边界明确，只有一个权威来源。
- 策划可见字段具备项目语言标签、说明、单位和约束；代码标识符保持英文。
- 自定义Inspector使用序列化API，Undo、多选和Prefab Override可用。
- 字段改名／删除、枚举排序和资产升级有迁移策略。
- 验证器能定位具体资产、对象和字段，并给出可执行修复提示。
