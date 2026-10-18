# 游戏技术路线

本指南按REA 6.7.0正式发布包及其随附技能重建，不声明新增游戏格式解析能力。上游与许可见插件根目录`THIRD_PARTY_NOTICES.md`及`licenses/rea-MIT.txt`。使用当前连接实际提供的工具与参数，不因本文列名就假设可用。

技术细节按需读：[原生／托管／归档](upstream-rea/references/native-and-artifacts.md)、[JavaScript](upstream-rea/references/javascript-applications.md)、[Android](upstream-rea/references/android-applications.md)、[运行观察](upstream-rea/references/runtime-observation.md)、[证据分页与验证](upstream-rea/references/evidence-workflows.md)。无需把全部通用技术路线逐项运行一遍。

## 先识别，再选路线

| 材料／目标 | 路线 | 限制 |
| --- | --- | --- |
| 完整源码、CSV／JSON、规则文档 | 常规文件／代码工具，先找注册、加载和调用方 | 不必启用REA；数据值不自动等于生效值 |
| Godot导出／PCK | 清点引擎和包头版本；使用已可用且版本兼容的专用提取／恢复工具 | REA通用归档支持不能当作PCK支持；没有工具就报告格式缺口。恢复脚本可能丢类型、注释或控制流 |
| Unity Mono | 确认Managed程序集与资源清单；REA的`inspect_managed_artifact`查托管身份／元数据，按已提供能力进一步追踪 | 元数据不等于完整C#方法恢复；资产解析用实际可用的版本兼容工具 |
| Unity IL2CPP、Unreal或其他原生游戏 | 身份与库／数据清单→已配置原生分析provider→相关函数／引用／配置 | IL2CPP不是可直接按Mono还原的CIL；Unreal容器／加密需要各自支持，不假定可提取或规避密钥保护 |
| ZIP／APK等支持的普通归档 | `open_binary`绑定后`inspect_artifact`，需要落地时`extract_artifact` | 仅在格式被支持时使用；工具当前返回的临时提取目录为准，不虚构自选输出参数 |
| JavaScript／Electron／ASAR | `analyze_javascript_application`；按支持的`detail: summary`和选定源码范围读摘要，再追踪相关模块 | 范围外代码保持未知；源码映射／可读化不等于原始工程 |
| Android游戏APK | 按实际工具用`inspect_android_package`及聚焦类／方法检查；原生库另走原生路线 | Java／JADX等外部前提不会随技能安装；APK声明不等于运行行为 |
| 本地WASM及JS胶水 | 有对应工具和WABT时`inspect_wasm_artifact` | WAT不是原始源码，不隐式下载或执行网页 |
| 原生EXE／DLL | `open_binary`后函数、字符串、交叉引用与伪代码；需要时才用`binary_overview` | provider可能不可用；伪代码、地址与字符串只能支持对应范围的推断 |
| 已有录像／日志／存档快照 | 时间戳／操作／初始状态追踪；静止副本上解析 | 不主动修改真实存档；SQLite快照如含WAL需保留一致性与身份 |

## REA证据处理

直接调用最能回答问题的工具；只在provider／会话状态不清或发生变化时查`binary_session`。它返回的能力与不可用原因不是所有引擎已安装的证明。先摘要再按实际Evidence ID／node_id分页；同一路径可能对应不同模块角色，不用模糊路径代替身份。

保留返回的`evidence_id`、`normalized_result`、限制、覆盖和未知。结果截断时用实际返回的父Evidence ID请求`inspect_analysis_view`或导出完整证据，不解析截断预览为完整JSON，也不重复同一个生产调用来“重试读完”。关闭会话前按需要导出：保留ID通常不能跨连接复用。

版本比较必须身份兼容、完整度可比；全量对侧覆盖不足时不能断言新增／删除。有限重建验证只证明声明的可比较断言，不代表整个游戏等价。

## 运行验证

先声明问题、初始状态、操作、预期区分的结果、最长时间／次数及退出办法。用户演示、录像观察、代理实际操作分开标注。普通游戏窗口使用当前可用的计算机／引擎工具，不声称REA能控制任意游戏。

网页／Electron仅在已有合法目标和支持的连接条件下使用REA：用户操作时可被动观察；代理操作须用显式动作方案。`capture_browser_scenario`连接模式可能先导航并丢失临时状态；执行前说明影响。运行与探针不是沙箱，可能写文件或联网；不为了验证一个掉落规则启动无关进程、购买、多人匹配或账户操作。

随机实验记录样本量、种子可控性和候选条件，不能把未掉落当零概率。实际游戏不允许或无法复核时，交付静态证据和建议实验，不编造运行结果。
