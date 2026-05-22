# 风险状态向量 \\(\mathbf{w}=\{L_{\mathrm{act}},L_{\mathrm{des}},\sigma,\phi,\mathbf{z},\eta\}\\) 物理量详解

## 主表

| 符号 | 物理量 | 含义 | 值域/类型 | 计算依据 | 备注 |
|------|--------|------|-----------|---------|------|
| **\\(L_{\mathrm{act}}\\)** | 输出风险等级 (Active Level) | 经迟滞滤波稳压后的最终风险等级 | `NONE(0)` / `NOTICE(1)` / `WARNING(2)` / `EMERGENCY(3)` | 对\\(L_{\mathrm{des}}\\)施加迟滞滤波：即时升级、延时降级（默认1s保持） | 论文公式中的稳压输出，用于下游控制映射 |
| **\\(L_{\mathrm{des}}\\)** | 期望风险等级 (Desired Level) | 静态风险与动态风险的原始融合最大值 | 同上四档 | `max(static\_level, dynamic\_level)` | 反映传感器原始融合结果，未经迟滞处理 |
| **\\(\sigma\\)** | 风险来源归因 (Risk Source) | 引发当前风险的主导因素类型 | `"clear"` / `"static"` / `"dynamic"` / `"combined"` / `"system"` | `classifySource()`: 比较static_level与dynamic_level | 控制策略依据不同来源选择不同响应方式 |
| **\\(\phi\\)** | 触发机理说明 (Trigger Reason) | 触发当前风险等级的具体物理原因 | 见"触发机理枚举表" | `buildReason()`: 根据各指标与阈值关系判定 | 包含源种类前缀如 `visual/...`、`cylinder/...` |
| **\\(\mathbf{z}\\)** | 证据向量 (Evidence Vector) | 支撑风险判定的多维度量化证据 | 包含5个子项（见"证据向量子项表"） | — | 对应"距离、相对运动与时域预测" |
| **\\(\eta\\)** | 系统有效性 (System Ready) | 系统输入是否满足有效性约束 | `true` / `false` | 检测感知输入是否缺失、跟踪是否超时 | 为控制决策提供系统健康状态依据 |

## \\(\mathbf{z}\\) 证据向量子项

| 子项 | 类型 | 含义 | 阈值体系 (Notice/Warning/Emergency) |
|------|------|------|--------------------------------------|
| `static_clearance` | float (m) | 静态障碍物最近距离 | 5.0 / 3.0 / 1.0 |
| `dynamic_clearance` | float (m) | 动态目标当前距离 | 5.0 / 3.0 / 1.0 |
| `relative_speed` | float (m/s) | 与动态目标的相对接近速度 | —（辅助指标） |
| `ttc` | float (s) | 与动态目标的预计碰撞时间 | 6.0 / 3.0 / 1.5 |
| `predicted_clearance` | float (m) | 预测时域终点处的预测净距 | 5.0 / 3.0 / 1.0 |
| `head_on` | bool | 是否检测到对头碰撞模式 | —（标志位，触发升级） |

## \\(\phi\\) 触发机理完整枚举

| \\(\phi\\) 取值 | 含义 | 触发条件 |
|----------------|------|---------|
| `"clear"` | 无风险 | 所有指标均未超限 |
| `"static_clearance_threshold"` | 静态净距低于阈值 | `clearance <= threshold` 且点云支撑充足 |
| `"static_sparse_points"` | 静态净距超限但点云稀疏 | `clearance <= threshold` 但支撑点不足，仅报NOTICE |
| `"dynamic_current_clearance"` | 动态当前净距触发 | `current_clearance <= threshold` |
| `"dynamic_predicted_clearance"` | 动态预测净距触发 | `predicted_clearance <= threshold` |
| `"dynamic_ttc_emergency"` | TTC紧急触发 | `ttc <= emergency_ttc`（仅EMERGENCY级别） |
| `"dynamic_head_on_upgrade"` | 对头碰撞升级 | `head_on == true` 且当前级别低于WARNING |

**来源前缀组合**（\\(\phi\\) 实际格式为 `<source_kind>/<reason>`）：
- `visual/...` — 视觉检测（YOLO分割）目标触发的风险
- `cylinder/...` — 吊钩圆柱体包络体触发的风险

## 关键代码位置

| 组件 | 文件 | 行号 |
|------|------|------|
| WarningState.msg 定义 | `main_ros_code/src/LIO-SAM-MID360/msg/WarningState.msg` | 1-21 |
| 风险分级枚举 | 同上 | 1-4 |
| SourceEvaluation 结构体 | `main_ros_code/src/LIO-SAM-MID360/src/warningEvaluator.cpp` | 153-168 |
| DynamicRiskMetrics 结构体 | 同上 | 113-123 |
| \\(L_{\mathrm{des}}\\) 融合计算 | 同上 | 915 |
| 迟滞滤波 \\(L_{\mathrm{des}} \rightarrow L_{\mathrm{act}}\\) | 同上 | 1682-1706 |
| \\(\sigma\\) 来源分类 `classifySource()` | 同上 | 1709-1721 |
| \\(\phi\\) 原因生成 `buildReason()` | 同上 | 1723-1752 |
| 静态分级 `classifyStaticLevel()` | 同上 | 1642-1660 |
| 动态分级 `classifyDynamicLevel()` | 同上 | 1662-1680 |
| 阈值配置文件 | `main_ros_code/src/LIO-SAM-MID360/config/warning_evaluator.yaml` | 52-65 |
