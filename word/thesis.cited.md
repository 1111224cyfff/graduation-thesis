# 题目：基于雷视融合的塔吊吊装过程动态避障与预警方法研究

# 第1章 引言

## 1.1 研究背景

建筑业作为关系国计民生的基础性产业，是国民经济的重要组成部门。据国家统计局发布的《中国统计年鉴2023》数据显示，2022年建筑业总产值为83383.1亿元，占国内生产总值的6.9%\cite{E78S579E}。在建筑施工作业中，塔式起重机是建筑施工现场中使用最广泛的垂直运输设备，具有起重高度高、作业范围广、工作效率高等优势\cite{G8HEXPSB,3LHPNGFB,CSVHSWVZ}，其吊装作业承担着钢筋笼、模板、物料等关键构件的吊运任务。然而，塔吊施工环境普遍存在空间狭窄、视野受限、动态干扰因素复杂等特点，加之运行高度大、工作半径长，一旦发生碰撞或人员误入吊装路径，其后果往往极为严重。根据统计，2014年至2022年间全国起重机事故数量不低于220起；其中，吊物伤人与物体碰撞类事故累计超过75起，占比显著且发生频率较高\cite{KWVSPS3W}。因此，如何实现吊装过程的实时环境感知与风险预警，是当前智慧工地安全管理中亟需攻克的重要问题之一。

近年来，随着建筑智能化与智能建造理念的提出，基于传感器的数据感知技术得到了快速发展，为施工过程数据采集的实时性和自动化需求提供了潜在的解决方案\cite{9LK3VTEQ}。大量研究集中于塔吊塔身或塔臂端的防碰撞系统，例如对多塔协同作业的塔臂干涉检测、塔机与周边建筑结构的距离监测等。然而，这类研究大多基于固定位置的传感器布置，主要关注塔臂或塔身层面的宏观防碰撞问题，而对实际吊装环节中最危险的部位塔吊吊钩端关注显著不足。

吊钩端是吊装过程中运动最频繁、最接近人员和构件的部位，其作业特点具有以下显著特征：（1）空间运动高度不确定：吊钩随吊臂回转、钢丝绳伸缩及外力扰动持续发生三维空间运动，摆幅可达数米，传统固定式传感器难以覆盖其动态空间范围。（2）近场作业风险极高：大量施工人员需要在吊运构件下方或附近进行配合作业，人员无意靠近吊钩、吊物摆动、构件碰撞均可能造成重大安全事故。（3）环境遮挡复杂且光照变化剧烈：钢筋笼、模板体系等大型构件会造成相机视野遮挡，而工地环境存在尘土、夜间照明等不利因素，对视觉系统效果影响显著。（4）传统方法难以实现实时、可落地的近场避障：现有塔吊安全系统普遍依赖塔身安装的超声、雷达或视觉设备，其检测范围难以覆盖吊钩周围 3\~5 米的高危近场区域，使得关键危险点无法及时识别。

随着轻量化激光雷达和高性能嵌入式计算平台的快速发展，为塔吊吊钩端构建实时空间感知系统提供了技术基础。激光雷达具备高精度距离测量能力，能够在强光、弱光、粉尘等复杂工况中保持稳定输出，并可实现高达360°的水平视场（FoV），从而覆盖吊钩周围的全方位近场空间。相比之下，视觉传感器具有丰富的语义理解能力，特别是在识别施工人员、车辆等关键危险目标方面具有显著优势。因此，构建"雷达为主、视觉为辅"的雷视融合感知架构能够充分结合两类传感器的互补特性，为实现塔吊吊钩端的实时、可靠避障预警系统创造了可行条件。

基于上述背景，本研究面向吊钩端高风险作业场景，选用激光雷达与工业相机设计并开发集成式吊钩端感知系统，以实现对近场三维环境的高精度感知与危险目标识别，减少施工现场吊装作业中的碰撞风险、保障人员生命安全，也为建筑施工装备的数字化、智能化升级提供了一种可落地、可推广的技术路径，具有重要的工程应用价值和现实意义。

## 1.2 研究目的与意义

### 1.2.1 研究目的

针对塔吊吊装作业中吊钩端近场空间运动不确定、风险集中、环境干扰复杂等核心痛点，以及现有安全感知系统对吊钩端覆盖不足、单一传感器鲁棒性差、预警精度与实时性难以兼顾的问题，本研究旨在实现以下目标：

1.  设计并构建一套可工程化落地的吊钩端集成式感知系统，通过激光雷达与工业相机的协同部署，突破传统传感器在覆盖范围、环境适应性上的局限，实现对吊钩周围 3\~5 米高危近场区域的全方位、高精度感知。

2.  提出基于雷视融合的多源数据处理与信息融合方法，整合激光雷达的三维几何测距优势与视觉传感器的语义识别能力，实现静态障碍精准建模、动态目标（尤其是施工人员）可靠识别与轨迹跟踪。

3.  建立兼顾空间距离与时间裕度的动态风险评估模型，形成 "感知 - 识别 - 预判 - 预警" 的闭环机制，实现对碰撞风险的分级预警与动态避障辅助决策，提升预警的提前量与准确性，降低误报、漏报率。

4.  验证系统在复杂施工工况下的稳定性、实时性与工程适用性，为塔吊吊装作业安全防护提供可推广、可复用的技术方案。

### 1.2.2 研究意义 

建筑业塔吊吊装事故频发，给人员生命安全与工程财产造成严重损失。本研究聚焦吊钩端这一最高风险区域，通过构建实时感知与预警系统，可直接减少人员误入、吊物碰撞等恶性事故发生概率，为施工现场安全管理提供技术保障。同时，系统采用轻量化硬件集成与高效算法设计，兼顾部署成本与运行稳定性，适配施工场地粉尘、震动、光照多变等恶劣环境，具备较强的工程落地性，可快速推广至各类建筑施工场景，推动塔吊装备的智能化升级，助力智慧工地建设。

现有塔吊安全感知研究多集中于塔身、塔臂等宏观层面，对吊钩端动态近场感知的研究较为匮乏。本研究提出 "雷达为主、视觉为辅" 的雷视融合架构，完善了多传感器在高危作业端的部署与标定方法，丰富了动态复杂场景下近场感知的理论体系。同时，研究建立的静动态目标分离、轨迹预测与分级预警模型，为多源数据融合在工程装备安全防护中的应用提供了新的思路，填补了吊钩端高精度、高鲁棒性感知技术的研究空白，为同类大型工程机械的安全智能化提供了理论参考与技术借鉴。

随着智能建造理念的深入推进，施工装备的数字化、智能化成为行业发展必然趋势。本研究通过传感器集成、数据融合与智能算法的深度结合，实现了吊装作业从 "被动防护" 向 "主动预警" 的转变，契合建筑行业安全升级与效率提升的核心需求。研究成果不仅可应用于塔吊设备，还可迁移至履带吊、汽车吊等其他起重机械，为工程机械行业的智能化转型提供典型示范，推动建筑业向安全、高效、智能的方向高质量发展。

## 1.3 国内外研究现状

随着智能建造与施工现场数字化水平的不断提升，工程机械与大型吊装设备的安全感知与智能防护逐渐成为国内外学术界和工程界的研究热点。围绕施工设备运行安全，已有研究主要集中在作业环境信息获取以及碰撞风险识别与预警等方面，形成了从感知、理解到决策的多层次研究体系。然而，由于施工现场环境复杂、目标类型多样、作业过程动态性强，现有研究在感知对象、传感器布置位置以及安全防护粒度等方面仍存在一定局限，尤其在塔吊等大型起重设备的吊钩端动态作业区域，相关研究尚不充分。

### 1.3.1 吊装感知硬件布置方案研究

[突出：吊钩端研究匮乏，研究方法可延伸]{.mark}

吊装作业是施工现场最常见的高危作业之一。为防范作业过程中可能对人员或建筑构件造成的损害，众多学者致力于通过智能感知技术与传感器部署来提升作业安全性。例如，在塔吊吊臂、小车、驾驶室及施工现场周边等位置，布设摄像机\cite{FIQUTEC5}、惯性测量单元（Inertial Measurement Unit，IMU）\cite{NN865XZQ,FWEHHUWL}、射频识别（RFID）\cite{E97V5FCY}、超宽带（Ultra Wide Band，UWB）\cite{9LK3VTEQ}、超声波传感器\cite{TWWSPDKK}、高度传感器\cite{U3E4PYX6}、风速传感器\cite{2URRPIZ4}等多种传感器，以实时监测作业状态、识别周边障碍物与人员，从而实现风险预警。

值得注意的是，传感器布设方案（含布设位置、传感器选型及集成方式）与传感精度直接决定环境感知效果，而感知数据作为后续风险识别、动态避障等算法判断的核心输入依据，其质量优劣直接影响决策的准确性与可靠性。不同布设位置、不同类型传感器所获取的数据，在感知范围、实时性、抗干扰性等方面存在显著差异，因此科学优化传感器布设方案，是提升吊装作业智能防护水平的关键前提。

[（配套安置在塔吊多个关节的传感器，几何关系联立得到位置信息）]{.mark}

在实际施工现场，多台塔吊交叉作业的场景普遍存在，作业空间交错复杂，极易引发塔吊间结构干涉、吊物与周边物体碰撞等叠加风险。早期塔吊防碰撞研究多依赖塔机自身运行参数进行间接判断，其中部分方案的传感器布设虽未直接聚焦塔臂，但为后续塔臂布设方案提供了基础思路。例如，周飞虎\cite{USJ52UW5}在塔机回转机构、变幅机构与起升机构等关键部位布设角度、幅度与高度传感器，采集塔机姿态与运行状态数据，通过几何关系推算吊钩位置及构件相对关系，将潜在碰撞转化为构件间几何距离与阈值的比较以触发预警。

进一步地，Zhong等\cite{VNWJWSIA}从工程应用角度出发，构建了一套基于无线传感器网络（WSN）与物联网（IoT）的塔吊群安全管理系统。该系统在塔吊关键结构部位布设多类型传感器节点，包括塔臂、小车及起升机构等位置，用于采集塔吊运行状态与作业参数，并通过无线传感器网络实现多塔设备之间的数据传输与集中管理。传感器采集的数据主要包括塔臂回转角度、小车位置、吊钩高度等信息，系统基于这些参数在统一坐标系下对塔吊结构的空间关系进行计算，从而判断塔吊之间是否存在潜在的干涉或碰撞风险。当相关参数超过预设安全阈值时，系统通过物联网平台向操作人员发送预警信息，实现对塔吊群作业安全状态的实时监控。

[（安装在塔臂&小车&驾驶室）]{.mark}

针对塔吊间碰撞预警，Hwang 等\cite{9LK3VTEQ}在实验室环境下搭建了两个缩尺塔吊模型，在每台塔吊吊臂前端和后端各布置1个UWB 标签，并在实验场地角点固定布设 UWB 接收器，通过AoA与TDoA相结合的方式获取标签的空间位置信息。基于塔吊轴向旋转的运动特性，该方法采用标签间距离作为等效几何约束，将塔吊结构之间的安全距离映射为标签距离阈值，从而实现塔吊间潜在碰撞的实时预警。但该方案的传感器仍仅布设于塔吊结构本体，未在吊钩或吊物上增设独立感知单元，因此无法覆盖吊物与环境障碍物之间的碰撞风险，感知范围存在明显局限。（监控塔吊群的塔臂碰撞）

为直接感知吊臂周边障碍物，赵宇\cite{R5GR6N2A}提出了一种基于超声波传感与无线组网的塔吊防碰撞方案，沿吊臂方向在吊臂关键位置均匀安装多个节点式超声波探测器阵列，用于实时感知吊臂周围障碍物的距离信息。由于单个超声波传感器视场角有限，该方法通过阵列化布设扩大探测范围，在吊臂周围形成连续的线性保护区域，可直接实现吊臂与障碍物之间的碰撞判断。同时，依靠部署在塔机回转机构和起升机构等关键部位的高度、角度传感器来获取吊物高度及塔身回转角度等参数，融合后推算出吊装物体的空间位置，从而**间接实现**吊装物体与障碍物之间的碰撞预警，但这样的方式仍存在因吊索与吊物摆动导致的定位偏差问题。

Zhou等\cite{I2FL5SGE}将GNSS接收机固定于塔吊小车的支撑框架顶部，实时获取各塔吊塔臂端部在统一坐标系下的空间位置信息，从而实现对多塔空间关系的持续监测。基于 GNSS 解算得到的平面坐标数据，系统将塔臂简化为几何线段，并通过计算不同塔吊塔臂之间的相对距离来评估潜在的碰撞风险，当距离小于预设安全阈值时触发相应的碰撞预警。该方法通过引入 GNSS 定位传感器提升了多塔作业环境下的空间感知能力，但其传感器布设仍主要集中于塔吊结构本体，防碰撞对象以塔臂之间的结构干涉为主，未对吊钩或吊装物体进行直接感知。

张知田等\cite{XBDUPUTH}提出面向"塔吊---工人"空间交互的危险场景自动检测框架，通过**工人位置**与**吊钩（等效吊物）位置**的同步获取实现预警。硬件布设上，该方法在**塔吊驾驶室下方架设远视角摄像头**以捕捉作业面内工人分布，同时在**吊臂滑动小车下方安装垂直向下摄像头**以估计吊钩/吊物的水平摆动偏移，并在塔吊主体布设**角度与测距传感器**获取吊臂旋转/下压角及小车、吊钩关键距离参数，通过局域网络实现数据实时传输。基于多源数据融合，方法先由图像估计吊钩偏移，再结合角度/测距数据计算吊钩三维坐标，并将工人与吊钩位置映射至 BIM 模型；在判别层面，以吊钩垂直投影点为中心构建10 m 圆形半径的动态危险区域，当工人进入该区域即触发危险场景预警。

上述方法中，传感器布设集中于塔机本体吊臂、小车等平台，工程部署难度低、成本可控，但因未直接感知周边环境，对周围障碍物及吊装作业的直接风险缺乏有效感知能力。且它们大都通过传感数据组合联立，以计算出如吊钩、吊臂的特定位置，并与障碍物计算相对距离。这些方法中，传感器的布设大都集中于塔吊结构本体，未对吊钩或吊装物体进行直接感知，存在xx问题。因此，部分工作进一步将传感设备（或可被可靠观测的靶标）**直接部署在吊钩端/吊钩块/吊物**，以更直接获取端部真实运动状态并提升预警可靠性。

[（安装在吊钩）]{.mark}

Lee 等\cite{J95BVZBC}在塔吊盲吊导航系统中，将吊钩块作为关键观测对象：在变幅臂端安装激光传感器，并在**吊钩块安装反射板**作为测距靶标，利用激光束反射测得臂端到吊钩块的实际垂直距离。考虑到吊钩块剧烈摆动会导致"错失反射板"而产生误测，系统进一步结合吊钩块运动速度与方向对异常数据进行滤除，同时以放绳长度编码器作为备份测量源，最终将多源位置与视频信息发送至**驾驶室内的导航服务器**并在 BIM 模型中实时显示吊物位置与周边环境关系，主要用于提升盲吊场景下的态势感知与导航辅助。

在此基础上，为更直接表征"吊钩端摆动/旋转"等动态风险，Fang 等\cite{K9J9CXIH}提出将**无线 IMU 刚性安装在吊物或吊钩端载荷上**，由 IMU 测得吊物的欧拉旋转角，在已知吊绳长度并近似刚性的前提下，可将姿态角进一步转换为吊物在三维空间中的相对位置，从而实现对吊物摆动状态的在线监测，并与编码器等机构传感数据结合用于安全辅助与告警。

不过，相关综述也指出这类"端部直测"方案往往要求在吊物/吊钩块/吊钩上增加额外硬件，带来电池维护、现场粗放工况下的损伤风险，以及金属环境对无线链路的干扰等工程约束。

进一步地，Ku 等\cite{J95BVZBC}在机器人化塔吊系统中将"吊钩块"视为末端执行器，直接在**吊钩块安装 3D LiDAR**获取近场点云以感知周围结构与潜在障碍，并将点云处理流水线部署在**吊钩块上的工业计算机**中实时提取路径方向上的障碍高度等关键信息，处理结果再无线回传至驾驶室内主机用于决策与避障执行。

除此之外，由于摄像机轻便的特性，许多研究者也尝试将摄像机安置于吊钩端，对下方拍摄感知，实现如施工危险对象识别\cite{MHXEXK6X}、工人与负载碰撞预警\cite{R625G22I}等塔吊安全监测与预防研究。

### 1.3.2 施工现场环境感知方法研究

施工现场环境感知是塔吊安全预警与避障控制的基础，其核心在于在复杂、动态且强不确定的工况下持续获取"设备自身状态---作业空间几何---人员与障碍物信息"，并据此进行风险评估与提示。现有研究与工程应用中，塔吊相关感知传感器大体可按信息来源划分为三类：一类用于获取塔吊本体或吊钩端的运动状态与空间位姿，为后续感知与预警提供统一参考；第二类用于感知作业环境中的几何距离与空间结构，支撑安全距离判断与危险区域入侵检测；第三类用于获取目标的语义或身份信息，尤其是对工人等高风险对象的识别与管理。不同传感器在测量维度、精度、部署成本与环境鲁棒性方面存在显著差异，也决定了其在塔吊避障系统中常见的组合方式与融合层级选择。早期研究主要探索不同类型传感器在感知问题上的应用，随着研究不断深入以及感知判断要求的不断提升，多源传感器融合方式为提高系统鲁棒性、准确性提供了良好的解决办法。

（1）传感技术

（整理表格）

编码器（包含角度、高度等状态传感器）常用于获取塔吊自身的状态，通过获取回转半径和回转角度等信息，能够步步推算出小车位置、吊钩高度以及结构关键部位的运动边界信息。该类传感器可靠性高、成本低、工程布置成熟，能够为塔吊运动学模型、作业包络计算与禁行区生成提供直接输入，是典型的"间接感知"手段。然而其测量对象**主要是设备自身状态**，难以感知外部环境中临时出现的障碍物、人员靠近以及吊物周边的局部复杂结构，因此通常需要与外部环境传感器结合才能形成完整的避障能力。

惯性测量单元（IMU）能够提供角速度与加速度信息，在吊钩端强动态条件下用于运动状态估计、姿态变化监测以及对扫描类传感器（如LiDAR）进行运动畸变补偿。对于吊钩端避障场景，IMU的价值主要体现在两方面：其一，用于描述吊钩摆动、旋转等快速姿态变化，为点云稳定化与坐标系一致性提供支撑；其二，与其他传感器（如LiDAR、视觉、GNSS）融合形成更稳定的位姿估计。但IMU存在累计漂移，单独使用难以提供长期稳定的位置与姿态基准，通常需要与外部定位或地图约束结合。

GNSS（及RTK）常用于塔吊场景中的宏观定位与设备状态监测，例如塔吊基座或关键构件的绝对位置获取、施工区域级的空间约束建立等。RTK具备较高的平面定位精度，适用于开阔环境下的绝对坐标基准构建，也便于与BIM/施工组织规划进行空间对齐。然而在城市密集施工环境中，GNSS易受遮挡与多径效应影响，且对吊钩端等局部高动态部位的精细定位支撑有限；此外，GNSS本身无法直接感知障碍物几何边界，因此更适合作为全局参考或与IMU、LiDAR等共同构建多传感器定位框架。

UWB定位系统在施工安全管理领域应用较多，典型方式是在工人佩戴标签、现场布置基站，从而实现人员定位、电子围栏与区域入侵告警。UWB的优势在于可对人员提供显式定位信息，便于实现"人"的风险管理与统计，并且可与塔吊作业区域规则进行结合。但UWB系统部署依赖基站布设与标定，定位精度与稳定性受环境遮挡、金属结构、多径效应影响明显；同时UWB难以描述障碍物的几何形状与边界，通常更适合作为人员高危提示或辅助决策信息，而非替代基于几何测距的避障感知。

RFID技术在塔吊作业中更多用于构件、吊具或物料的身份识别与流程管理，例如对吊装构件进行唯一标识、实现装卸与流转记录、辅助吊装任务调度与追溯。在安全预警层面，RFID可用于识别"正在吊装的对象是什么"、与作业权限或工序规则联动，从而在管理层面增强安全性。但RFID通常难以提供稳定连续的空间位置与距离信息，其通信距离、读写可靠性也受金属遮挡与现场电磁环境影响，因此更适合作为"身份/状态信息源"融入系统，而非用于实时几何避障判定。

视觉作为一种信息丰富且价格便宜的信息获取方式，在语义理解方面具有明显优势，能够直观区分不同目标类别，且硬件成本较低、部署灵活。由于塔吊操作员的特殊工作位置导致不可避免存在实现盲区，早期的研究者们就已经尝试在塔吊上部署视觉系统\cite{KC3A3Q33}以显示吊装的负载和下方的工作区域，让在驾驶室的操作员能够直观看到吊钩端的情况，减少视觉盲区。如今，随着计算机技术发展，通过结合传统图像处理方法或深度学习算法，能够实现施工对象的目标检测，在此基础上可以实现吊物空间姿态测量\cite{U6D69PTF}、生产效率统计\cite{MIA77CU2}、工人运动轨迹监测\cite{R625G22I}等任务。然而，视觉感知方法对光照条件和环境遮挡较为敏感，在夜间作业、强光或复杂遮挡条件下感知性能容易下降，同时难以直接获取精确的空间距离信息，在安全距离判断等应用中存在一定局限。与普通相机相比，深度相机及结构光相机能够直接提供局部深度信息，适合近距离空间测量与区域入侵检测，但在强光环境、远距离以及室外复杂工况下稳定性和测距范围会受到限制，其适用边界需要结合具体作业场景评估。

毫米波雷达具备全天候工作能力，对雨雾粉尘等恶劣工况鲁棒，且对运动目标具有较强敏感性，在夜间或能见度较低场景中具有优势。其不足在于角分辨率与空间细节表达能力通常不如LiDAR，难以精确刻画复杂障碍物的几何边界，因此在塔吊避障中更常用于冗余检测、近距离存在性判断或对运动目标的补充提示，而非单独承担精细空间建模任务。

超声波传感器成本低、实现简单，适合极近距离防撞与边界触发（例如小范围防护或特定方向的距离阈值检测）。但其测距范围有限，受传播介质、风噪与环境干扰影响较大，且难以覆盖吊钩端大范围三维空间，因此更多作为近距冗余或辅助触发传感器，与其他三维传感器配合使用。

激光雷达（LiDAR）能够输出三维点云并提供稳定的测距能力，是施工现场空间几何感知的关键传感器之一。对于塔吊避障而言，LiDAR可直接支持危险区域入侵判定、安全距离阈值触发、障碍物轮廓提取等任务，并且对光照变化不敏感，具备较高工程鲁棒性。但LiDAR对语义类别理解较弱，对"人"与"非人"的区分通常需要结合视觉或学习型算法；此外，金属反射、玻璃等材质以及遮挡引起的点云缺失、离群点等问题，需要配合滤波、聚类与一致性策略提高稳定性。因此在实际系统中，LiDAR常作为"测距与空间判定主传感器"，与其他语义或状态传感器形成互补。

（2）多传感器融合感知

在复杂施工现场，仅依赖单一传感器往往难以同时满足安全预警所需的**空间几何精度、语义理解能力与环境鲁棒性**。因此，多传感器融合逐渐成为施工环境感知的重要技术路线。一般而言，多传感器融合是指在统一的时间与空间参考框架下，对来自不同传感器的信息进行对齐、关联与组合，以获得更完整、更可靠的环境状态估计或风险判定结果。其本质目标可概括为两类：其一，通过不同模态信息的**互补性**提升感知维度（例如视觉提供语义、测距传感器提供几何距离）；其二，通过信息的**冗余性**增强系统可靠性与容错能力，从而降低施工现场不确定因素带来的误报与漏报。

在塔吊避障与安全管理领域，多传感器融合研究大体可以分为两类路径：一类面向**塔吊/吊钩端状态与位姿获取**，以编码器、限位、GNSS/RTK、IMU等为主要信息源，通过融合提升位姿连续性与全局参考稳定性，为作业包络计算、限制区生成与塔群协同防碰撞提供支撑。

许多研究者\cite{K9J9CXIH,NN865XZQ,8JDQ27IN,25XZJFDZ,5BYWKC7L,RBS3C7F5}明确了测量起重机操作的多个关键运动：吊臂回转角、提升绳伸长量和吊臂伸长量，并采用编码器、倾角传感器进行测量获取，以捕捉塔吊的运动状态。这种方式主要聚焦于布设于塔吊不同位置的传感器，根据每部分的参数通过建立塔吊的运动方程得到塔吊自身的状态，在原理上属于数据的拼接。仅依靠这些数据，在现实摆动的情况下无法准确估计吊钩和吊物的状态，这也是值得关注的高风险区域。对此，有通过线性激光装置测量塔吊小车到吊钩端的距离，再结合旋转编码器获取的旋转角度来得到吊物所在的位置\cite{RBS3C7F5}；也有在吊钩上侧金属壁安装IMU，并结合起重机的传感数据以捕捉吊钩的运动姿态（图1）\cite{K9J9CXIH}。而Price等\cite{NN865XZQ}考虑到吊物冲击较大时可能损坏传感器，采用了视觉系统来定位吊物的偏移和旋转，但是缺乏吊物的深度信息，仍通过传感获取的缆绳长度作为吊物高度的间接估计。

![](C:\Users\Lenovo\Desktop\graduation_thesis\word/media/image1.jpg){width="5.7140004374453195in" height="1.6659995625546806in"}

图1 Transforming the augular measurements to absolute positions

由于施工现场是一个动态复杂环境，必须将起吊现场环境数据集成到起吊辅助框架中，才能起到实际的安全防护作用，同时，由于起重机特有的运动属性，其覆盖范围不能仅考虑二维，而是要实现三维感知。而三维激光扫描技术为上述命题提供了一种解决方案。依托地面激光扫描仪或者无人机摄影测量技术\cite{G4AVEHSG}，可以获取工地范围内的3D点云数据，每个扫描点都包含了三维坐标信息及RGB颜色数据，可以表征场景中物体的几何形状。扫描后的点云经过点云降采样、分割、聚类和方向估计等步骤，对场景中各种对象形成定向边界框，形成一张静态地图并集成到安全预警系统中，随周期性的扫描进行更新\cite{NN865XZQ,K9J9CXIH}。但是这样的方式仍存在分辨率低和更新频率低的问题。同时，点云更新和扫描范围也是一个问题，每台塔吊有自己的工作范围，大面积的场景建模会扫描许多冗余点云，为场景点云更新和算法判断带来处理性能压力。

另一类路径面向**外部环境与人员风险识别**，更强调对障碍物几何距离与人员语义信息的联合获取。典型做法包括以激光雷达/毫米波雷达提供可靠测距与空间入侵判定，以视觉方法提供工人等高危对象的语义识别与可视化解释，并在决策层进行风险分级预警。在实际研究中，以避障为最终研究目的的研究，通常使用多个传感器，在实现塔身姿态的内部感知基础上，完成外界状态的外部感知。

在施工现场环境感知中，视觉传感器因能同步获取障碍物几何距离与人员语义信息的独特优势，成为多传感器融合系统的核心感知单元，相关研究围绕技术优化与工程适配展开了大量探索。

Yang 等\cite{8FY5FXQ3}采用 Mask R-CNN 对人员与障碍物进行语义分割，通过像素 - 实际距离转换模型，联合输出人员语义状态与安全距离，计算误差控制在 3% 以内；Golcarenarenji 等\cite{MHXEXK6X}设计的 CraneNet 深度学习模型，基于单目视觉实现 50 米范围内人员检测（语义识别）与远距离测量（几何距离），准确率达 92.59%，且在嵌入式设备上实现 19 FPS 的实时性，适用于起重机驾驶室等空间受限场景。这类方案的优势在于部署成本低、语义信息提取能力强，但测距精度受图像分辨率与特征提取质量影响，弱光环境下性能易下降。双目视觉方案则通过立体匹配直接获取障碍物距离，几何精度高于单目，同时结合 CNN 实现人员 / 设备语义分类，但其测量范围受基线长度限制，近距离遮挡时匹配困难，设备体积也大于单目视觉，更适用于固定监测点的近距离作业场景。

视觉与其他传感器的融合方案进一步提升了联合感知的鲁棒性与精度。视觉与激光雷达融合方案中，视觉负责人员、设备、障碍物的语义识别，激光雷达提供高精度几何距离与三维点云，通过特征级融合将距离特征融入视觉检测网络，有效弥补视觉测距精度不足与激光雷达语义信息匮乏的缺陷，Price 等\cite{T92DZ92V}基于该方案实现盲吊场景的障碍物距离与人员语义联合预警，适配高精度要求的复杂环境；视觉 + RFID/IMU 融合方案则利用 RFID/IMU 的精准定位能力（几何距离）与视觉的行为语义提取优势，通过决策级融合实现人员动态风险预警，Zhang 等\cite{G47UYPFK}采用 FairMOT 算法跟踪人员与吊具，结合 Transformer 模型预测轨迹，联合人员位置信息与移动语义，建立多等级碰撞风险预警规则，提升人员密集场景的风险识别可靠性。此外，聚焦人员风险识别的专项融合方案成为研究焦点，Shapira 等\cite{KC3A3Q33}的视觉系统通过人员检测与距离判断，在缩短起重机作业周期的同时降低安全风险。

（3）雷视融合感知

在智能交通、自动驾驶、智慧工地等复杂环境感知场景中，精准、实时、鲁棒地获取目标信息是系统安全运行的核心前提，雷达与视觉传感器作为核心感知载体各有优劣且高度互补------视觉传感器语义信息提取能力强、成本低、部署灵活，可精准识别目标类别、外观特征及场景细节，但易受光照、天气及遮挡影响，远距离测距测速精度不足；雷达具备高精度测距测速、抗干扰能力强等优势，激光雷达能输出精准三维点云，毫米波雷达适应恶劣天气且动态跟踪效果好，然激光雷达成本高昂、语义信息匮乏，毫米波雷达分辨率低、近距离小目标识别能力弱，而雷视融合技术通过数据级、特征级等合理融合策略整合二者数据，可借助视觉语义优势弥补雷达短板，同时依托雷达空间感知能力修正视觉偏差，显著提升复杂场景适应能力与感知鲁棒性，为决策控制提供全面精准的数据支撑。

从融合策略与信息处理层级出发，现有研究将雷视融合划分为数据级融合、特征级融合、目标属性级融合与决策级融合四类\cite{PL2G5AIL}。

数据级融合强调在原始数据层面实现信息联合，对多源测距数据进行坐标统一与点云拼接、对图像与深度/点云进行时空对齐后再进行联合建模。该策略的关键在于统一不同模态数据的表达尺度与坐标基准，从而在最底层最大化保留信息量，并为后续处理提供更一致的输入表示。Zhou和Omar\cite{IPIVFMW7}采用像素级融合红外图像与RGB图像，采用自适应加权平均算法处理非饱和像素数据，针对饱和像素区域（眩光场景）实施主成分分析（PCA）算法，将两种输入的图像融合为单一输入，实现图像增强，以更鲁棒地检测实际场景中出现的人员和障碍。由于雷达和图像在水平与垂直分辨率上远低于光学图像\cite{PL2G5AIL}，因此，需要在时空间上分别进行对齐，而非图像间的归一化像素级融合。Kim等\cite{6VLQ22DN}综合使用 GPS、毫米波雷达、LiDAR 与视觉构建环境表示，通过多帧 LiDAR 观测累积生成网格地图，并以栅格"障碍观测计数"超过阈值触发风险预警，同时用雷达候选目标与视觉识别目标交叉验证并更新静态地图与安全区域。Lekic 与 Babic\cite{6JL73W7F} 利用 GAN 将雷达信息生成环境图像并与光学图像融合，Ouyang 等\cite{9EZWD4IB}则使用条件 GAN 在图像监督下由点云重建语义场景图像，旨在缓解点云与相机直接融合带来的计算负担，并在 KITTI 数据集上验证实时检测有效性。

特征级融合通常先从各传感器数据中提取如几何特征、运动特征或深度网络特征的中间表示，再在特征空间完成联合建模，能够在信息利用与系统复杂度之间取得一定平衡，尤其在学习型感知框架中较为常见。传统机器学习时期往往需要先提取 HOG、GLCM 等人工特征，再用 SVM/AdaBoost 等分类器完成识别；而深度学习兴起后，特征融合更多被嵌入神经网络结构中，以端到端方式自动学习跨模态互补表示\cite{PL2G5AIL}。在雷视融合任务中，特征级融合常用于道路/可行驶区域检测等场景，例如Caltagirone 等\cite{2GFRMDA6}基于全卷积网络实现 LiDAR 与相机融合的道路检测。

更贴近工程避障预警需求的是目标属性级融合，各传感器先输出目标候选，再进行融合以降低单一传感器误报与漏报，该层级的抽象程度介于数据级融合与特征级融合之间，能够在保持计算可控的同时显著提升系统稳定性。一个与"吊钩端避障可视化"高度一致的范式是"LiDAR 生成 ROI → 图像中识别/解释 ROI"，如Wu等\cite{VWFQEPVD} 利用 LiDAR 的距离与角度信息在图像中生成 ROI，并结合 3D 点云形状信息进一步验证目标以降低误报、缓解遮挡带来的相机漏检。同时，该方法通过匹配 LiDAR 与图像端的目标列表来提升检测速度并获得较高的行人检测精度。Han 等\cite{B46NC5I5}从系统实现角度强调实时性与工程落地，为"点云候选 + 视觉解释"的在线管线提供了工程参考。类似地，Zhong 等\cite{IPFD4E6N}利用毫米波雷达运动信息提供图像 ROI，并在 ROI 上用 CNN 识别目标，同时合并雷达与相机的目标列表以提升鲁棒性。

决策级融合则由各传感器独立完成检测、识别或风险判定，再通过规则、置信度或逻辑推理进行融合输出，如采用贝叶斯推理、D-S 证据理论、模糊推理等。对工程避障而言，Wei 等\cite{Z8QR9XPU}直接面向工业场景的实时避碰系统，体现了"检测结果融合→避障决策"的应用导向。De Silva等\cite{687GA9DL}则强调在移动机器人平台上实现鲁棒融合。

综上所述，雷视融合研究的核心共识在于：通过融合激光雷达的高精度三维几何与测距能力以及相机的纹理与语义表达能力，可以在复杂动态环境中显著提升目标感知的完整性、鲁棒性与可解释性，并降低单一传感器在遮挡、光照变化或传感噪声下造成的误检与漏检风险。现有工作虽然在融合深度与实现形式上差异较大，但普遍强调"可靠的时空对齐与外参标定"是雷视融合有效性的基础，并在此之上形成从端到端学习到工程化组合的多样路线。进一步而言，面向安全预警与避障等工程任务，雷视融合的研究趋势并非一味追求更深的网络耦合，而是更强调在实时性、系统复杂度与安全可靠性之间取得平衡：一方面利用几何信息实现稳定的距离与区域风险触发，另一方面用视觉语义增强对高风险目标的识别与可视化解释，从而构建"可落地、可维护、可扩展"的感知---预警闭环。

### 1.3.3 碰撞检测算法与预警模型研究

[可以先写路径规划的避障策略，再写实际工程方面]{.mark}

关于塔吊碰撞的检测与约束建模，既有研究首先在**塔吊吊装规划与虚拟仿真**场景中形成了较为系统的方法体系\cite{NEKKIG45}。在该场景下，研究人员多采用虚拟环境构建手段以模拟实际吊装场景，并以碰撞检测作为4D路径规划的约束条件\cite{KAVTM3MI}，如通过为塔吊构建定向包围盒（Oriented bounding box，OBB）\cite{6SVWRM5Y}，采用离散碰撞检测（Discrete Collision Detection，DCD）\cite{HZ3G3PMB,3T2HAT9Q}或最小距离计算\cite{8FRKDLAT}等方式判断碰撞是否发生。Lai和Kang\cite{39QNQEMU}中以简化外边界体（如球体、圆柱体等）近似现场机械与结构构件，从而显著降低实时碰撞检测的计算负担。这些方法在虚拟仿真环境下具有可行性，因为此时障碍物信息通常是已知且假设完全可观测的。但在实际场景中，周围环境的信息需要通过传感器实时获取，传感器的观测范围、精度以及数据延迟等问题，单纯依赖离线/静态几何模型的碰撞约束往往难以直接迁移。

针对施工过程中的实时安全辅助，研究逐渐从"是否碰撞"的二值判别，转向"**碰撞风险强度**"与"**分级预警**"建模。一类典型思路是构建安全包络或风险区域，采用最小距离/侵入判别触发告警\cite{KF34Y86G}。Wang等\cite{5JE9BPJQ}将风险区域与目标简化为AABB，并通过进入/逼近判别实现安全预警逻辑，体现了"几何包络 + 阈值规则"在实时系统中的工程可实现性。Yang等\cite{JSDZGAGY} 使用Mask R-CNN检测危险源并根据照片与实际的像素转换关系换算计算工人与危险源的安全距离。

更进一步的研究强调在作业过程中持续评估风险并向操作者提供主动式辅助，面向吊装作业的实时主动安全辅助框架的核心在于动态工作空间建模与风险提示机制，而非仅在碰撞发生时被动报警\cite{K9J9CXIH}。Fang等\cite{FWEHHUWL}进一步从人机协同角度讨论了安全风险呈现与操作者态势感知评估，为预警模型如何"可解释地"服务现场作业提供了参考。

当障碍物与塔吊/吊载存在相对运动时，仅以"当前距离是否小于阈值"进行判断可能出现两类问题：其一，两个目标距离尚大但存在快速相向趋势，风险会在短时间内迅速上升；其二，阈值设置过大又会带来高误报，影响作业效率。因此，很多研究引入时间域 surrogate risk 指标，将风险刻画从"空间距离"推进到"时间余量"，典型如 Time-to-Collision（TTC）等。虽然 TTC 最初广泛用于交通安全 surrogate measures 的研究语境，Nadimi等\cite{MAG8XRJ5}对 TTC 等指标的适用性与局限进行了系统讨论，为"时间裕度型预警阈值如何设定与解释"提供了可借鉴的建模思路。在吊装场景下，将 TTC 类思想与相对速度/加速度估计结合，可形成"距离---速度联合预警"的框架，使预警更关注"是否会在未来短时窗内进入危险区"，而非仅关注当前几何接触。

根据Kim等\cite{XULW2BE3}的研究，相较于预防邻近的事故，预测潜在的碰撞事故能够更为有效地避免危险。。围绕预测驱动的碰撞预警，研究通常先对作业对象进行短时轨迹预测，再对未来时窗内的碰撞可能性进行判别或分级。张冬\cite{3FJ56MZB}将碰撞预警方式区分为两种形式：针对塔吊与静止建筑物的碰撞，考虑为基于距离的预警；而针对塔吊与塔吊之间的碰撞，在距离模型的基础上结合速度模型来进行综合判断。进一步地，轨迹预测方法本身也形成了从统计模型到深度学习模型的谱系，例如通过隐马尔可夫模型（Hidden Markov Model，HMM）\cite{TC4V9RAC}、长短期记忆人工神经网络（Long Short-Term Memory，LSTM）\cite{HRDHH5IM}、深度神经网络 (Deep Neural Network，DNN)\cite{TF9IX4KK} 等对人员或障碍物运动进行建模与预测。在获得塔吊与障碍物的未来轨迹后，可通过综合分析双方的相对运动趋势来进行风险判断，例如采用基于碰撞锥\cite{UHXM7SNP,BHEQBQYN}、基于约束优化等方法\cite{UYMXPTM6}。

除风险度量模型外，动态场景下的碰撞检测还面临"实时性---精度/漏检风险"的工程折中问题。为此，相关研究在算法实现上通常采用"分层剔除 + 精细检测"的策略。在吊装路径规划与动态环境中，Dutta等\cite{HZ3G3PMB}提出了近实时重规划模块，并在决策支持部分采用多层级 OBB 来进行风险相关的判别与触发，体现了"层次包围体 + 决策逻辑"在动态场景中的可扩展性。Zhu等\cite{YMH5BX8M}强调为提高碰撞检测效率与精度，需要融合空间划分与层次包围体等策略，并讨论了连续碰撞检测（CCD）在吊装扫掠体场景下的重要性。同样地，Lin等\cite{97BJ5NLW}提出基于点云的碰撞检测方法并将其嵌入规划流程，反映出"直接用现场环境状态驱动碰撞判别"的趋势。

在更一般的动态避碰理论中，碰撞风险还可通过"相对速度可达集合"进行刻画，例如碰撞锥（collision cone）与速度障碍（velocity obstacle, VO）范式。Fiorini and Shiller早在**1998年便**提出了 VO 框架以在动态环境中选择规避机动\cite{BZUL7ZKB}，其思想可用于将塔吊端执行体与动态障碍的相对运动关系显式化。Van den Berg等\cite{25CQDW8W}将该思想扩展到多主体实时避碰，为复杂多障碍、多作业体并行施工条件下的风险判别提供了更系统的理论工具。进一步地，安全关键建模常将避碰问题表述为"满足安全集约束"的控制问题，控制障碍函数（CBF）成为近年来重要方向之一。Jian等\cite{QG5TNYGE}提出了D-CBF，将障碍物预测与安全约束结合，用以保证动态避障的可行性与安全性，这为"预警模型如何与后续控制/干预策略耦合"提供了可迁移的建模范式。

综上，塔吊碰撞检测与预警模型研究呈现出从"仿真/规划约束下的几何碰撞判别"向"面向施工过程的分级预警"再到"时间裕度与预测驱动风险评估"的演进趋势。一方面，距离/包络等几何判别仍是预警触发的基础，但在动态场景下需结合时间裕度指标与轨迹预测以提升提前量并降低误报；另一方面，为实现在线运行，碰撞检测算法本身也趋向采用层次包围体、空间划分与连续碰撞检测等策略来兼顾效率与漏检风险。上述研究为后续构建面向塔吊作业的实时碰撞预警系统提供了可复用的方法基础，同时也提示预警模型需要在提前量、误报/漏报、实时性与鲁棒性之间进行系统权衡。

### 1.3.4 文献总结

综合国内外研究现状，围绕塔吊吊装安全的感知硬件布置、环境感知方法、碰撞检测与预警模型三大核心方向，现有研究已形成一定的技术积累，但仍存在以下关键不足，为本文研究提供了明确的切入点：

1.  **感知硬件部署聚焦不足**：现有传感器布置多集中于塔吊塔身、塔臂或施工现场固定位置，以宏观防碰撞为目标，对吊钩端这一最高风险区域的直接感知研究匮乏。虽有少数研究尝试在吊钩端部署传感设备，但存在硬件维护困难、抗干扰能力弱、感知范围有限等问题，难以满足近场全方位、高精度感知需求。

2.  **环境感知方法存在局限**：单一传感器感知存在明显短板（如视觉受光照影响、雷达语义匮乏），多传感器融合成为主流趋势，但现有融合方案或过于依赖复杂深度学习模型导致实时性不足，或仅停留在数据拼接层面未能充分发挥互补优势。针对施工场景的雷视融合研究，尚未形成兼顾几何精度、语义识别与工程鲁棒性的成熟方案，尤其缺乏针对吊钩端动态特性的适配优化。

3.  **预警模型适配性不足**：现有碰撞检测算法多源于虚拟仿真或路径规划场景，依赖静态几何模型，难以应对施工现场动态干扰多、障碍物复杂的实际情况；预警机制多基于单一空间距离阈值，未充分结合目标运动趋势与时间裕度，易出现误报或预警滞后问题。同时，对施工人员等高风险目标的语义关联不足，难以实现精准分级预警。

## 1.4 主要研究内容

（包括方法一共有哪些部分，每部分逻辑关系，每一部分的介绍，以及论文的结构）

本文围绕"基于雷视融合的塔吊吊装过程动态避障与预警方法研究"这一主题，面向塔吊吊钩端近场作业过程中"空间狭窄、遮挡复杂、目标动态性强、操作视野受限"等典型特征，构建以激光雷达空间测距为主、视觉语义识别为辅的在线碰撞风险判定与分级预警方法体系。具体研究内容包括：

**（1）吊钩端传感器系统构建**

针对吊钩动态作业特性，完成了多传感器硬件集成与一体化防护设计，包括双激光雷达与工业相机选型与布局优化。基于ROS构建通信链路，实现多传感器标定（内参、外参）、时间同步与延迟补偿，建立统一坐标系与TF体系，为后续处理提供可靠数据基础。

**（2）基于融合点云的定位与空间危险区域检测方法**

基于双雷达融合点云，实现吊钩端精准定位与危险区域感知。采用LIO-SAM完成SLAM定位与静态地图构建，通过点云预处理与时序分析分离静动态点云，结合聚类与卡尔曼滤波跟踪动态目标。构建"吊物尺寸+圆柱并集"动态危险区域模型，通过交集检测与连贯性验证输出危险区域信息。

**（3）基于雷视融合的避障预警策略**

融合激光雷达几何信息与视觉语义检测，提出分级预警方法。通过视觉检测时序稳定化处理，设计双向一致性融合策略实现目标轨迹级关联。针对静态障碍采用距离阈值预警，对动态目标构建"距离-时间"双维度风险评估模型，结合TTC与轨迹预测实现三级分级预警，提升预警准确率与鲁棒性。

## 1.5 技术路线

（图）

# 第2章 吊钩端传感器系统构建与配准

## 2.1 系统总体架构与硬件选型布置

### 2.1.1 传感设备选型

[双 LiDAR + 工业相机，说明选型依据：视场覆盖、语义识别需求]{.mark}

### 2.1.2 安装布局优化

LiDAR 盲区互补、相机视场协同

### 2.1.3 吊钩端一体化盒体设计

（工程可落地性：震动、粉尘、线缆、通信/计算/供电）

## 2.2 多传感器外参标定

### 2.2.1 相机内参标定

### 2.2.2 双雷达外参自动标定与精配准

（已完成：粗配准+自动精配准→变换矩阵）

### 2.2.3 雷达--相机外参标定

（为第4章投影关联做铺垫）

## 2.3数据链路与接口规范

### 2.3.1 通信链路搭建

（双网口/桥接/转发逻辑、传输稳定性）

### 2.3.2 时间同步与延迟补偿

（LiDAR/相机/IMU，时序一致性保障）

### 2.3.3 坐标系与 TF 接口规范

（空间参考约定，不涉融合细节）

# 第3章 基于融合点云的定位与空间危险区域检测方法

还有另一个问题。对于扫描后点云的预处理工作是在lio-sam前进行还是lio-sam后进行？

## 3.1 双雷达点云实时融合方法

### 3.1.1 原始点云数据特征

### 3.1.2 外参矩阵应用与坐标统一

设有两个右手直角坐标系 $\{ a\}$与 $\{ b\}$。

从坐标系 $\{ a\}$出发，通过一系列**绕自身坐标轴的旋转（内旋，intrinsic rotation）和一次自身坐标系下的平移**，得到坐标系 $\{ b\}$。

目标是求坐标系 $\{ a\}$到 $\{ b\}$的齐次变换矩阵：

$$\mathbf{T}_{a}^{b} = \lbrack\begin{matrix}
\mathbf{R}_{a}^{b} & \mathbf{t}_{a}^{b} \\
\mathbf{0}^{\mathsf{T}} & 1
\end{matrix}\rbrack$$
本文中**所有旋转均为绕当前自身坐标轴的旋转（内旋）**。

若一系列内旋旋转按照顺序依次执行，则**总旋转矩阵等于各旋转矩阵按顺序右乘**：

![](C:\Users\Lenovo\Desktop\graduation_thesis\word/media/image2.png){width="1.4901410761154856in" height="0.3311428258967629in"}

绕 $z$,y轴旋转

![](C:\Users\Lenovo\Desktop\graduation_thesis\word/media/image3.wmf)

![](C:\Users\Lenovo\Desktop\graduation_thesis\word/media/image4.wmf)

从坐标系 $\{ a\}$出发，旋转顺序如下（均为内旋）：

1.  绕自身 $z$轴旋转 $180^{\circ}$

2.  绕自身 $y$轴旋转 $- 30^{\circ}$

3.  再次绕自身 $y$轴旋转 $- 30^{\circ}$

由于两次旋转均绕同一轴，可以合并角度：

$$- 30^{\circ} + ( - 30^{\circ}) = - 60^{\circ}$$

因此总旋转可写为：

![](C:\Users\Lenovo\Desktop\graduation_thesis\word/media/image5.wmf)

![](C:\Users\Lenovo\Desktop\graduation_thesis\word/media/image6.wmf)

![](C:\Users\Lenovo\Desktop\graduation_thesis\word/media/image7.wmf)

![](C:\Users\Lenovo\Desktop\graduation_thesis\word/media/image8.wmf)

在完成**前两步旋转**后，沿**当前自身坐标系的** $x$**轴负方向**平移：169.204874mm（177.140239mm）

在自身坐标系下的平移向量为：

![](C:\Users\Lenovo\Desktop\graduation_thesis\word/media/image9.wmf)

若平移向量在**旋转后的局部坐标系中定义**，则需通过旋转矩阵转换到参考坐标系：

![](C:\Users\Lenovo\Desktop\graduation_thesis\word/media/image10.wmf)

其中：

![](C:\Users\Lenovo\Desktop\graduation_thesis\word/media/image11.wmf)

最终结果

![](C:\Users\Lenovo\Desktop\graduation_thesis\word/media/image12.wmf)

整体最终结果

![](C:\Users\Lenovo\Desktop\graduation_thesis\word/media/image13.wmf)

![](C:\Users\Lenovo\Desktop\graduation_thesis\word/media/image14.wmf)

![](C:\Users\Lenovo\Desktop\graduation_thesis\word/media/image15.wmf)

![](C:\Users\Lenovo\Desktop\graduation_thesis\word/media/image16.wmf)

### 3.1.3点云实时融合与发布

## 3.2 基于融合点云的SLAM定位与静态地图构建（LIO-SAM）

### 3.2.1 算法选择理由与系统输入输出

### 3.2.2 LIO-SAM流程

（前端里程计、后端因子图/回环等按实现程度写）

### 3.2.3 位姿输出与点云去畸变/配准

（与后续危险检测的关系）

## 3.3 面向目标提取的点云标准化与静动态目标生成

这一节明确：只产出"目标"（静态障碍表征 + 动态簇候选），不做风险判定。

### 3.3.1 近场关注区域ROI裁剪与点云预处理

（ROI裁剪、滤波、下采样、离群点抑制；强调实时性与鲁棒性）

### 3.3.2 基于位姿的时空对齐与局部滑窗表示

（利用 3.2 位姿做坐标统一；滑窗累积作为背景参考/时序容器）

### 3.3.3 静动态点分离与动态点云簇提取

（时序一致性/地图一致性；聚类输出动态簇中心、尺寸、包围盒）

### 3.3.4 目标短时跟踪与状态量估计

（卡尔曼/匀速模型；输出速度、轨迹，为趋势预测服务）

# 第4章 基于雷视融合的避障预警策略

## 4.1 视觉侧高风险目标识别

### 4.1.1 工人检测模型与部署 

（实时性、输入分辨率、输出格式）

### 4.1.2 检测结果时序稳定化处理

为降低单帧检测抖动对后续融合与预警的影响，对工人检测结果进行时序稳定化处理。

利用相邻帧检测框的重叠度与中心距离完成帧间匹配，为连续目标分配一致的 track_id；

引入短时丢检容错机制，当目标在连续不超过 M 帧内未被检测到时，仍保持其轨迹并使用上一时刻位置/预测位置进行补偿；

对检测置信度进行滑动平均并采用双阈值滞回策略实现目标"确认---消失"的稳定切换，从而输出连续、鲁棒的工人候选集合，为后续雷视目标关联提供可靠输入。

视觉置信度 s_det 做滑动平均：s̄\_det(t) = α s̄\_det(t-1) + (1-α) s_det(t)

s̄\_det \> Th_on 才把目标升级为"可信工人"

s̄\_det \< Th_off 才降级/移除

### 4.1.3 点云动态目标融合接口与数据结构定义

对视觉检测输出进行统一接口建模。对每一帧图像，工人检测模块输出候选集合 $\mathcal{D(}t)$，其中每个候选包含检测框坐标 $bbox = (u_{\min},v_{\min},u_{\max},v_{\max})$、检测置信度 $s_{\det}$以及由时序稳定化模块分配的 track_id。融合模块以时间戳为索引，将图像检测集合与同一时刻的点云动态目标集合进行匹配；其中外参矩阵与投影模型直接采用第2章标定结果。该接口设计保证了视觉信息以"门控区域 + 语义置信度 + 轨迹ID"的形式参与融合，从而在不引入高复杂度三维语义重建的前提下，实现对动态目标的人员语义增强与关联验证。

## 4.2 雷视融合策略

（从"能投影"到"能关联"）双向一致性关联与轨迹级语义增强

### 4.2.1 融合总体流程与设计原则

（LiDAR主几何、视觉提供语义与验证）

### 4.2.2 双相一致性关联策略

2D→3D门控关联（从检测框到点云候选）+3D→2D反向验证（从动态簇到图像一致性确认）

### 4.2.3 轨迹级绑定与遮挡鲁棒融合

（2D track ↔ 3D track）

### 4.2.4 置信度融合与语义标签输出

（human / non-human / unknown + score）

Score:融合视觉置信度、点云动态性、点数密度、时序稳定性，形成一个置信度打分机制

## 4.3 风险判定与分级预警策略

距离阈值 + 运动趋势预测

### 4.3.1 静态障碍：基于距离/侵入的阈值预警

（用第3章的危险域判定结果，距离/侵入阈值、滞回）

### 4.3.2 动态目标：基于相对速度/轨迹预测的碰撞风险

（TTC/最小距离时刻等）

### 4.3.3 分级预警状态机

（Normal/Warning/Danger，滞回与抑制误报）

# 第5章 实验验证与系统评估

## 5.1 实验平台与测试场景设置

### 5.1.1 吊钩端实验平台构成

### 5.1.2 典型测试工况设计

## 5.2 多传感器定位性能实验

### 5.2.1 位姿解算精度验证

### 5.2.2 吊钩动态摆动场景分析

## 5.3 雷视协同感知效果分析

### 5.3.1 工人检测准确性评估

### 5.3.2 雷视关联一致性分析

## 5.4 危险区域检测效果验证

### 5.4.1 静态障碍场景测试

### 5.4.2 动态人员接近场景测试

## 5.5 系统实时性与稳定性验证

### 5.5.1 各模块耗时分析

### 5.5.2 工程应用可行性分析

# 第6章 结论与展望

## 6.1 主要研究结论

## 6.2 创新点总结

## 6.3 存在的不足与未来展望

参考文献

\[1\] 中华人民共和国国家统计局. 2023 中国统计年鉴\[M\]. 北京：中国统计出版，2023.\[M\].

\[2\] 肖智珺.塔式起重机智能路径规划研究\[D\].太原科技大学,2023.\[J\].

\[3\] Shapira A, Lyachin B. Identification and Analysis of Factors Affecting Safety on Construction Sites with Tower Cranes\[J\]. Journal of Construction Engineering and Management, 2009, 135(1): 24-33.

\[4\] Shapira A, Lucko G, Schexnayder C J. Cranes for Building Construction Projects\[J\]. Journal of Construction Engineering and Management, 2007, 133(9): 690-700.

\[5\] 张达. 2014年---2022年塔式起重机安全事故案例统计分析\[J\]. 建筑安全, 2025, 40(2): 81-85.

\[6\] Hwang S. Ultra-wide band technology experiments for real-time prevention of tower crane collisions\[J\]. Automation in Construction, 2012, 22: 545-553.

\[7\] Ali A H, Zayed T, Wang R D, 等. Tower crane safety technologies: A synthesis of academic research and industry insights\[J\]. Automation in Construction, 2024, 163: 105429.

\[8\] Price L C, Chen J, Park J, 等. Multisensor-driven real-time crane monitoring system for blind lift operations: Lessons learned from a case study\[J\]. Automation in Construction, 2021, 124: 103552.

\[9\] Fang Y, Cho Y K, Durso F, 等. Assessment of operator's situation awareness for smart operation of mobile cranes\[J\]. Automation in Construction, 2018, 85: 65-75.

\[10\] Chae S, Yoshida T. Application of RFID technology to prevention of collision accident with heavy equipment\[J\]. Automation in Construction, 2010, 19(3): 368-374.

\[11\] Zhang C, Hammad A, Rodriguez S. Crane Pose Estimation Using UWB Real-Time Location System\[J\]. Journal of Computing in Civil Engineering, 2012, 26(5): 625-637.

\[12\] 郁志明. 塔吊安全监控系统的设计与研究\[D/OL\]. 东北大学, 2019\[2025-12-30\]. https://kns.cnki.net/KCMS/detail/detail.aspx?dbcode=CMFD&dbname=CMFD201901&filename=1019029559.nh.

\[13\] 张伟, 廖阳新, 蒋灵, 等. 基于物联网的塔式起重机安全监控系统\[J\]. 中国安全科学学报, 2021, 31(2): 55-62.

\[14\] 周飞虎. 塔式起重机防碰撞技术与安全监控系统研究\[D/OL\]. 长安大学, 2016\[2025-12-30\]. https://kns.cnki.net/KCMS/detail/detail.aspx?dbcode=CMFD&dbname=CMFD201601&filename=1015802742.nh.

\[15\] Zhong D, Lv H, Han J, 等. A Practical Application Combining Wireless Sensor Networks and Internet of Things: Safety Management System for Tower Crane Groups\[J\]. Sensors (Basel, Switzerland), 2014, 14(8): 13794-13814.

\[16\] 赵宇. 塔吊群作业无线组网技术与防碰撞算法研究\[D/OL\]. 哈尔滨理工大学, 2017\[2025-12-30\]. https://kns.cnki.net/KCMS/detail/detail.aspx?dbcode=CMFD&dbname=CMFD201701&filename=1016072789.nh.

\[17\] School of Geomatrics and Urban Spatial Information, Beijing University of Civil Engineering and Architecture, Beijing, China. Miao Wang is with School of Civil and Transportation Engineering, Beijing University of Civil Engineering and Architecture, Beijing, China., Zhou M, Wang Q, et al. Research on Intelligent Anti-collision Monitoring for Construction Tower Crane Group Based on GNSS Sensors\[J\]. International Journal of Computer and Communication Engineering, 2019, 8(4): 169-177.

\[18\] 张知田, 王园园, 罗柱邦, 等. 塔吊与工人空间交互下危险场景自动检测\[J\]. 清华大学学报（自然科学版）, 2024, 64(2): 198-204.

\[19\] Ku T K X, Zuo B, Ang W T. Robotic tower cranes with hardware-in-the-loop: Enhancing construction safety and efficiency\[J\]. Automation in Construction, 2024, 168: 105765.

\[20\] Fang Y, Cho Y K, Chen J. A framework for real-time pro-active safety assistance for mobile crane lifting operations\[J\]. Automation in Construction, 2016, 72: 367-379.

\[21\] Golcarenarenji G, Martinez-Alpiste I, Wang Q, et al. Machine-learning-based top-view safety monitoring of ground workforce on complex industrial sites\[J\]. Neural Computing and Applications, 2022, 34(6): 4207-4220.

\[22\] Zhang M, Ge S. Vision and Trajectory--Based Dynamic Collision Prewarning Mechanism for Tower Cranes\[J\]. Journal of Construction Engineering and Management, 2022, 148(7): 04022057.

\[23\] Shapira A, Rosenfeld Y, Mizrahi I. Vision System for Tower Cranes\[J\]. Journal of Construction Engineering and Management, 2008, 134(5): 320-332.

\[24\] Xing-yu F, Dan N, Qi L, et al. Position-pose measurement of crane sway based on monocular vision\[J\]. The Journal of Engineering, 2019, 2019(22): 8330-8334.

\[25\] Jeong I, Hwang J, Kim J, 等. Vision-Based Productivity Monitoring of Tower Crane Operations during Curtain Wall Installation Using a Database-Free Approach\[J\]. Journal of Computing in Civil Engineering, 2023, 37(4): 04023015.

\[26\] Sleiman J P, Zankoul E, Khoury H, 等. Sensor-Based Planning Tool for Tower Crane Anti-Collision Monitoring on Construction Sites\[J\]. 2016: 2624-2632.

\[27\] Yong Y P, Lee S J, Chang Y H, et al. Object Detection and Distance Measurement Algorithm for Collision Avoidance of Precast Concrete Installation during Crane Lifting Process\[J\]. Buildings, 2023, 13(10): 2551.

\[28\] Fang Y, Chen J, Cho Y K, 等. Vision-based load sway monitoring to improve crane safety in blind lifts\[J\]. Journal of Structural Integrity and Maintenance, 2018, 3(4): 233-242.

\[29\] Lee G, Kim H H, Lee C J, 等. A laser-technology-based lifting-path tracking system for a robotic tower crane\[J\]. Automation in Construction, 2009, 18(7): 865-874.

\[30\] Siebert S, Teizer J. Mobile 3D mapping for surveying earthwork projects using an Unmanned Aerial Vehicle (UAV) system\[J\]. Automation in Construction, 2014, 41: 1-14.

\[31\] Yang Z, Yuan Y, Zhang M, et al. Safety Distance Identification for Crane Drivers Based on Mask R-CNN\[J\]. Sensors, 2019, 19(12): 2789.

\[32\] Price L C, Chen J, Park J, 等. Multisensor-driven real-time crane monitoring system for blind lift operations: Lessons learned from a case study\[J\]. Automation in Construction, 2021, 124: 103552.

\[33\] Zhang M, Ge S. Vision and Trajectory--Based Dynamic Collision Prewarning Mechanism for Tower Cranes\[J\]. Journal of Construction Engineering and Management, 2022, 148(7): 04022057.

\[34\] Wang Z, Wu Y, Niu Q. Multi-Sensor Fusion in Automated Driving: A Survey\[J\]. IEEE Access, 2020, 8: 2847-2868.

\[35\] Zhou Y, Omar M. Pixel-Level Fusion for Infrared and Visible Acquisitions\[J\]. International Journal of Optomechatronics, 2009, 3(1): 41-53.

\[36\] Kim B, Kim D, Park S, 等. Automated Complex Urban Driving based on Enhanced Environment Representation with GPS/map, Radar, Lidar and Vision\[J\]. IFAC-PapersOnLine, 2016, 49(11): 190-195.

\[37\] Lekic V, Babic Z. Automotive radar and camera fusion using Generative Adversarial Networks\[J\]. Computer Vision and Image Understanding, 2019, 184: 1-8.

\[38\] Ouyang Z, Liu Y, Zhang C, 等. A cGANs-Based Scene Reconstruction Model Using Lidar Point Cloud\[C/OL\]//2017 IEEE International Symposium on Parallel and Distributed Processing with Applications and 2017 IEEE International Conference on Ubiquitous Computing and Communications (ISPA/IUCC). 2017: 1107-1114\[2026-01-08\]. https://ieeexplore.ieee.org/abstract/document/8367397.

\[39\] Caltagirone L, Bellone M, Svensson L, 等. LIDAR--camera fusion for road detection using fully convolutional neural networks\[J\]. Robotics and Autonomous Systems, 2019, 111: 125-131.

\[40\] Wu T E, Tsai C C, Guo J I. LiDAR/camera sensor fusion technology for pedestrian detection\[C/OL\]//2017 Asia-Pacific Signal and Information Processing Association Annual Summit and Conference (APSIPA ASC). 2017: 1675-1678\[2026-01-08\]. https://ieeexplore.ieee.org/abstract/document/8282301.

\[41\] Han X, Lu J, Tai Y, 等. A real-time LIDAR and vision based pedestrian detection system for unmanned ground vehicles\[C/OL\]//2015 3rd IAPR Asian Conference on Pattern Recognition (ACPR). 2015: 635-639\[2026-01-08\]. https://ieeexplore.ieee.org/abstract/document/7486580.

\[42\] Zhong Z, Liu S, Mathew M, et al. Camera Radar Fusion for Increased Reliability in ADAS Applications\[J\]. Electronic Imaging, 2018, 30: 1-4.

\[43\] Wei P, Cagle L, Reza T, et al. LiDAR and Camera Detection Fusion in a Real-Time Industrial Multi-Sensor Collision Avoidance System\[J\]. Electronics, 2018, 7(6): 84.

\[44\] De Silva V, Roche J, Kondoz A. Robust Fusion of LiDAR and Wide-Angle Camera Data for Autonomous Mobile Robots\[J\]. Sensors, 2018, 18(8): 2730.

\[45\] Zhang Z, Pan W. Lift planning and optimization in construction: A thirty-year review\[J\]. Automation in Construction, 2020, 118: 103271.

\[46\] Chi H L, Kang S C. A physics-based simulation approach for cooperative erection activities\[J\]. Automation in Construction, 2010, 19(6): 750-761.

\[47\] Kuchkuda R. An Introduction to Ray Tracing\[C\]//EARNSHAW R A. Theoretical Foundations of Computer Graphics and CAD. Berlin, Heidelberg: Springer, 1988: 1039-1060.

\[48\] Dutta S, Cai Y, Huang L, 等. Automatic re-planning of lifting paths for robotized tower cranes in dynamic BIM environments\[J\]. Automation in Construction, 2020, 110: 102998.

\[49\] Zhu A, Zhang Z, Pan W. Crane-lift path planning for high-rise modular integrated construction through metaheuristic optimization and virtual prototyping\[J\]. Automation in Construction, 2022, 141: 104434.

\[50\] Yang B, Zhang H, Shen Z. Minimum Distance Calculation Method for Collision Issues in Lifting Construction Scenarios\[J\]. Journal of Computing in Civil Engineering, 2024, 38(6): 04024041.

\[51\] Lai K C, Kang S C. Collision detection strategies for virtual construction simulation\[J\]. Automation in Construction, 2009, 18(6): 724-736.

\[52\] Wu H, Tao J, Li X, 等. A location based service approach for collision warning systems in concrete dam construction\[J\]. Safety Science, 2013, 51(1): 338-346.

\[53\] Wang C C, Wang M, Sun J, et al. A Safety Warning Algorithm Based on Axis Aligned Bounding Box Method to Prevent Onsite Accidents of Mobile Construction Machineries\[J\]. Sensors, 2021, 21(21): 7075.

\[54\] Nadimi N, Behbahani H, Shahbazi H. Calibration and validation of a new time-based surrogate safety measure using fuzzy inference system\[J\]. Journal of Traffic and Transportation Engineering (English Edition), 2016, 3(1): 51-58.

\[55\] Zhu A, Zhang Z, Pan W. Developing a fast and accurate collision detection strategy for crane-lift path planning in high-rise modular integrated construction\[J\]. Advanced Engineering Informatics, 2024, 61: 102509.

\[56\] Lin X, Han Y, Guo H, 等. Lift path planning for tower cranes based on environmental point clouds\[J\]. Automation in Construction, 2023, 155: 105046.

\[57\] Fiorini P, Shiller Z. Motion Planning in Dynamic Environments Using Velocity Obstacles\[J\]. The International Journal of Robotics Research, 1998, 17(7): 760-772.

\[58\] van den Berg J, Lin M, Manocha D. Reciprocal Velocity Obstacles for real-time multi-agent navigation\[C/OL\]//2008 IEEE International Conference on Robotics and Automation. 2008: 1928-1935\[2026-01-08\]. https://ieeexplore.ieee.org/abstract/document/4543489.

\[59\] Jian Z, Yan Z, Lei X, et al. Dynamic Control Barrier Function-based Model Predictive Control to Safety-Critical Obstacle-Avoidance of Mobile Robot\[EB/OL\]//arXiv.org. (2022-09-18)\[2026-01-08\]. https://arxiv.org/abs/2209.08539v1.

\[60\] Yang Z, Yuan Y, Zhang M, et al. Safety Distance Identification for Crane Drivers Based on Mask R-CNN\[J\]. Sensors, 2019, 19(12): 2789.

\[61\] Kim D, Liu M, Lee S, et al. Trajectory Prediction of Mobile Construction Resources Toward Pro-active Struck-by Hazard Detection\[C/OL\]//36th International Symposium on Automation and Robotics in Construction. Banff, AB, Canada, 2019\[2026-01-08\]. http://www.iaarc.org/publications/2019_proceedings_of_the_36th_isarc/trajectory_prediction_of_mobile_construction_resources_toward_pro_active_struck_by_hazard_detection.html.

\[62\] 张冬. 塔式起重机智能监控系统研究与开发\[D/OL\]. 上海交通大学, 2020\[2026-01-08\]. https://doi.org/10.27307/d.cnki.gsjtu.2016.001713.

\[63\] Rashid K, Datta S, Behzadan A. Coupling risk attitude and motion data mining in a preemtive construction safety framework\[M\]. 2017: 2424.

\[64\] Tang S, Golparvar-Fard M, Naphade M, 等. Video-Based Motion Trajectory Forecasting Method for Proactive Construction Safety Monitoring Systems\[J\]. Journal of Computing in Civil Engineering, 2020, 34(6): 04020041.

\[65\] Kim D, Lee S, Kamat V R. Proximity Prediction of Mobile Objects to Prevent Contact-Driven Accidents in Co-Robotic Construction\[J\]. Journal of Computing in Civil Engineering, 2020, 34(4): 04020022.

\[66\] Sunkara V, Chakravarthy A. Collision avoidance laws for objects with arbitrary shapes\[C/OL\]//2016 IEEE 55th Conference on Decision and Control (CDC). 2016: 5158-5164\[2026-01-08\]. https://ieeexplore.ieee.org/abstract/document/7799058.

\[67\] Park J, Cho N. Collision Avoidance of Hexacopter UAV Based on LiDAR Data in Dynamic Environment\[J\]. Remote Sensing, 2020, 12(6): 975.

\[68\] Zhang X, Liniger A, Borrelli F. Optimization-Based Collision Avoidance\[J\]. IEEE Transactions on Control Systems Technology, 2021, 29(3): 972-983.

\[69\] Vaswani A, Shazeer N, Parmar N, 等. Attention is All you Need\[C/OL\]//Advances in Neural Information Processing Systems: 卷 30. Curran Associates, Inc., 2017\[2026-01-08\]. https://proceedings.neurips.cc/paper_files/paper/2017/hash/3f5ee243547dee91fbd053c1c4a845aa-Abstract.html.

\[70\] Kim J. Control laws to avoid collision with three dimensional obstacles using sensors\[J\]. Ocean Engineering, 2019, 172: 342-349.

\[71\] Pfreundschuh P, Hendrikx H F C, Reijgwart V, 等. Dynamic Object Aware LiDAR SLAM based on Automatic Generation of Training Data\[C/OL\]//2021 IEEE International Conference on Robotics and Automation (ICRA). 2021: 11641-11647\[2026-01-08\]. https://ieeexplore.ieee.org/abstract/document/9560730.

\[72\] Alonso I, Riazuelo L, Murillo A C. MiniNet: An Efficient Semantic Segmentation ConvNet for Real-Time Robotic Applications\[J\]. IEEE Transactions on Robotics, 2020, 36(4): 1340-1347.
