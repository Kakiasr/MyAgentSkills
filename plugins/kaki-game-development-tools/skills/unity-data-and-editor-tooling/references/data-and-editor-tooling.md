# Unity数据与编辑器工具参考

本参考整理自用户提供的《Unity项目开发规范》，将其中项目偏好改写为可验证的默认基线。

## 数据载体选择

| 情况 | 优先载体 |
| --- | --- |
| 共享核心规则、与场景无关、需要独立平衡 | ScriptableObject或表格资产 |
| 与图像、碰撞、子节点和实例化结构强绑定 | Prefab组件 |
| 大量行、外部协作、需要批量差异比较 | CSV／JSON等表格，经导入验证 |
| 本局可变状态、冷却、库存、累计分数 | System／Actor／纯C#运行模型 |
| 动画速度、抖动、过渡等表现参数 | Presentation Config或局部组件 |

修改值会改变策略或核心公式时归入玩法配置；只影响表现时不要污染主配置。Prefab上的小型定义可接受，规模扩大或多Prefab共享时再拆Definition资产。

## 序列化字段

- 默认`[SerializeField] private`，只读属性对外暴露。
- 范围明确时使用`Min/Range`或自定义验证；Tooltip写明单位、方向和影响。
- 字段改名使用`FormerlySerializedAs`完成有期限迁移；废弃字段不永久堆积。
- 序列化枚举进入资产后使用显式数值，避免排序改变已有数据。
- `OnValidate`只做快速、确定、无副作用的约束，不启动运行流程或执行昂贵扫描。
- ScriptableObject不保存本局状态，也不在Play Mode意外污染资产。

## 中文Inspector

面向中文团队时，代码标识符保持英文，用户可见标签、分组、枚举和Tooltip使用中文。可以选择：

- 简单字段：自定义中文Label Attribute + PropertyDrawer。
- 条件字段、复杂列表和公式：每类Config的CustomEditor。
- 大型工具流程：UI Toolkit EditorWindow／Inspector。

CustomEditor必须通过`serializedObject`与`SerializedProperty`工作，验证Undo、多对象编辑和Prefab Override。条件不生效的字段隐藏或禁用。单位写入标签或Tooltip；公式同时说明输入、取整和正负方向。

“所有字段必须中文”只适用于明确采用中文创作界面的项目，不是通用Unity规则。多语言团队应服从项目语言规范。

## Prefab与验证器

Actor Prefab通常以根Actor、Collider、VisualRoot和可选交互／FX锚点组成；这不是固定层级。根Transform、Collider职责、Renderer排序、定义引用、动态对象的场景引用和升级链应可验证。

常见验证器：Scene Wiring、重复事件源、Prefab结构、Config范围／断链、Audio/FX绑定、字体与Fallback、Build Scenes。每条错误包含资产路径、对象、字段、规则ID和修复建议；批量修复默认先预览。
