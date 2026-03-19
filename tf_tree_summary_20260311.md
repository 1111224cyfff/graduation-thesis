# TF 树总结

## 1. 当前工程中的主 TF 树

根据运行时导出的 TF 图和当前参数配置，主干关系可以概括为：

```text
map
└── odom
    ├── base_link
    │   └── chassis_link
    │       ├── imu_link
    │       ├── velodyne
    │       └── navsat_link
    └── lidar_link
```

其中主链路是：

```text
map -> odom -> base_link
```

这也是 ROS 中最常见的定位/建图坐标关系。

---

## 2. 各坐标系的含义

### map
- 全局地图坐标系。
- 用来表达“机器人在全局地图中的位置”。
- 这个坐标系希望尽量稳定、长期一致。
- 如果系统做了回环、全局优化或 GPS 融合，最终修正通常体现在这个层级上。

### odom
- 里程计坐标系。
- 表达机器人相对于起始时刻附近的连续运动。
- 特点是：
  - 短时间内平滑、连续；
  - 长时间会累积漂移；
  - 一般不给它施加突变。
- 适合局部运动估计、连续位姿输出、点云去畸变等需要平滑运动的模块。

### base_link
- 机器人主体参考坐标系。
- 通常认为这是机器人“本体”的中心参考系。
- 机器人当前位置/姿态通常最终都要落到这个坐标系上。
- 在本工程里，LIO-SAM 配置将 `lidarFrame` 和 `baselinkFrame` 都设成了 `base_link`，说明算法层把激光雷达主参考系和机体参考系统一了。

### chassis_link
- 底盘坐标系。
- 由 `robot_state_publisher` 从 URDF 中发布。
- 它挂在 `base_link` 下面，用来继续连接 IMU、LiDAR、GPS 等传感器坐标系。

### imu_link
- IMU 传感器自身坐标系。
- 用来描述 IMU 在机器人结构中的安装位置和姿态。

### velodyne
- LiDAR 传感器坐标系。
- 虽然名字叫 `velodyne`，但在当前 URDF 中它充当激光雷达安装坐标系。

### navsat_link
- GPS / NavSat 传感器坐标系。

### lidar_link
- 从当前 TF 图看，它由建图优化节点单独挂在 `odom` 下。
- 这通常表示优化线程发布的某个 LiDAR 位姿结果。
- 它不是主控制链路上的标准主体坐标系，理解 TF 主结构时优先关注 `map -> odom -> base_link` 即可。

---

## 3. 为什么要有 `map` 和 `odom` 两层

这是 ROS 定位系统里非常关键的一点。

如果只有一个坐标系，就很难同时满足下面两个要求：

1. **位姿连续平滑，不跳变**；
2. **长期位置尽量正确，不随时间漂移**。

而实际上传感器里程计往往只能满足其中一部分：
- IMU 预积分、激光里程计、轮速计可以提供**平滑连续**的运动；
- 但这些方法积分久了会**漂移**。

所以系统把问题拆成两层：

### `odom -> base_link`
- 负责输出机器人当前的连续运动。
- 这一层尽量保持平滑。
- 即使有误差，也先允许它慢慢漂移。

### `map -> odom`
- 负责把已经漂移的 `odom` 系整体校正回全局地图。
- 如果系统检测到回环、全局约束或者 GPS 修正，就通过这一层去补偿。

这样组合后：

- 局部运动看起来仍然连续；
- 全局轨迹又能被慢慢修正回正确位置。

数学上可以写成：

$$
T_{map}^{base\_link} = T_{map}^{odom} \cdot T_{odom}^{base\_link}
$$

意思是：
- 机器人在 `map` 下的位姿 =
- `map` 到 `odom` 的变换 × `odom` 到 `base_link` 的变换。

---

## 4. 本工程里各 TF 的发布者

根据当前导出的 TF 图：

### `map -> odom`
- 发布者：`/lio_sam_imuPreintegration`
- 含义：把里程计坐标系放到全局地图坐标系中。

### `odom -> base_link`
- 发布者：`/lio_sam_imuPreintegration`
- 含义：输出机器人本体在里程计坐标系中的连续位姿。

### `odom -> lidar_link`
- 发布者：`/lio_sam_mapOptmization`
- 含义：优化线程输出的 LiDAR 相关位姿。

### `base_link -> chassis_link`
### `chassis_link -> imu_link`
### `chassis_link -> velodyne`
### `chassis_link -> navsat_link`
- 发布者：`/robot_state_publisher`
- 含义：根据 URDF 发布机器人刚体结构关系。
- 这些通常是静态或准静态变换。

---

## 5. 当前配置中的关键 frame 参数

LIO-SAM 参数中主要设置为：

- `lidarFrame: base_link`
- `baselinkFrame: base_link`
- `odometryFrame: odom`
- `mapFrame: map`

这说明：

1. 算法内部主要把 LiDAR 参考帧统一到 `base_link`；
2. 局部里程计输出放在 `odom`；
3. 全局地图输出放在 `map`。

---

## 6. URDF 中的刚体结构关系

URDF 定义的是机器人本体和传感器安装关系，对应静态结构：

```text
base_link
└── chassis_link
    ├── imu_link
    ├── velodyne
    └── navsat_link
```

这部分不是“机器人在空间中运动了多少”，而是“机器人各传感器彼此怎么安装”。

可以理解为：
- `map` / `odom` / `base_link` 更偏向定位与运动；
- `chassis_link` / `imu_link` / `velodyne` / `navsat_link` 更偏向机构安装关系。

---

## 7. 在 RViz 中怎么理解

### Fixed Frame 设为 `map`
- 看到的是全局一致的地图结果。
- 适合看建图、回环后轨迹、全局位置。

### Fixed Frame 设为 `odom`
- 看到的是局部连续运动。
- 适合关注短时间位姿变化和局部运动平滑性。

### 传感器数据常挂在 `base_link` 或其子坐标系下
- 例如 IMU、LiDAR、GPS。
- 它们最终都通过 TF 与 `map` / `odom` 关联起来。

---

## 8. 一个直观理解

可以把这几个坐标系想象成下面的关系：

- `base_link`：机器人自己身上的坐标系；
- `odom`：机器人出发后靠传感器积分得到的“局部参考系”；
- `map`：全局地图参考系；
- `map -> odom`：负责纠偏；
- `odom -> base_link`：负责平滑跟踪机器人运动。

所以：

- `odom` 更像“连续但会漂”的运动参考；
- `map` 更像“全局正确”的地图参考。

---

## 9. 本工程 TF 树的结论

本工程的 TF 结构可以概括成两部分：

### 运动主链
```text
map -> odom -> base_link
```

### 机器人结构链
```text
base_link -> chassis_link -> {imu_link, velodyne, navsat_link}
```

其中：
- `map -> odom` 负责全局校正；
- `odom -> base_link` 负责连续位姿；
- `robot_state_publisher` 负责传感器安装关系；
- `lidar_link` 是建图优化线程额外发布的 LiDAR 位姿分支。

---

## 10. 适合直接记住的一句话

**这个工程里，`odom` 是连续但会漂的局部运动坐标系，`map` 是经过全局约束后更稳定的地图坐标系，而 `base_link` 是机器人本体坐标系。**
