# YXLand 1.4.0

Minecraft Java Edition **1.12.2** 永久领地保护、玩家领地管理与管理员系统领域插件。

## 玩家领地核心规则

- 玩家领地只计算 X×Z 平面面积，Y 不参与额度或扩建费用。
- 创建成功后 XZ 矩形从 Y=0~255 全高度永久保护。
- 普通玩家默认基础额度 70 格；VIP/SVIP 示例默认 140/280。
- 扩建每净新增 1 格默认 1000 Vault 金币，并同步永久增加 1 格已购额度；缩小免费、不退款。
- 左键选择真实 A 点、右键选择真实 B 点；玩家移动不会改变框选范围。
- 两点完成后不会自动打开 GUI，必须手持圈地工具“蹲下 + 右键”进入创建/扩建确认界面。
- 绿色边界使用小粒子沿矩形四边贴地形起伏显示，不生成火焰墙、竖柱、多层线或内部填充。

## 1.4.0：独立管理员系统领域 AdminRegion

1.4.0 新增真正独立于玩家 `Land` 的 `AdminRegion`：

- 不占玩家 70 格额度。
- 不计玩家领地数量。
- 不收费。
- 使用独立 ID、模型、空间索引和管理员选区状态。
- 只有拥有 `yxland.admin.region` 的管理员可以创建和管理。

入口：

```text
/land admin
→ 系统领域
```

或：

```text
/land admin region
```

### 管理员圈地

系统领域使用独立管理员工具，操作与玩家新式圈地一致：

```text
左键 → A 点
右键 → B 点
A/B 完成后显示绿色贴地边界
手持管理员领域工具 + 蹲下 + 右键 → 打开创建界面
```

管理员选区与普通玩家选区完全隔离，不会相互覆盖。

## 系统领域优先级

系统领域允许重叠，但规则固定为：

- **优先级数字越高越优先**。
- 不同优先级系统领域可以重叠。
- **同优先级系统领域发生重叠时禁止创建或调整**，避免最终规则不确定。

例如：

```text
主城        priority 10
└ 市场      priority 20
└ NPC区     priority 30
└ PVP竞技场 priority 50
```

玩家站在竞技场时优先读取 priority 50 的系统领域规则。

## 三态规则

AdminRegion 的规则不是简单 true/false，而是：

```text
INHERIT  继承
ALLOW    允许
DENY     禁止
```

解析顺序：

1. 从当前位置最高优先级系统领域开始。
2. 遇到显式 ALLOW / DENY 就使用该结果。
3. 遇到 INHERIT 则继续检查下一层较低优先级系统领域。
4. 所有系统领域都 INHERIT 后，才回落原有玩家领地/野外规则。

这样高优先级子区域只覆盖管理员明确修改过的规则，不会意外把下面的玩家私人领地全部放开。

## 系统领域可管理规则

包括：

- 方块破坏
- 方块放置
- 容器
- 常见交互
- 红石
- 桶
- PVP
- 实体伤害
- 进入
- 爆炸
- 火焰
- 液体
- 活塞
- 自动机器 / Inventory 自动化
- FakePlayer
- **PLAYER_CLAIM：是否允许玩家创建私人领地**

`PLAYER_CLAIM` 同样按优先级/INHERIT 解析，因此可以实现“大主城禁止圈地，但高优先级公共住宅子区域重新允许圈地”。

## 用途模板

系统领域支持快速套用用途模板，例如：

- 安全区
- NPC区域
- 资源区域
- 副本区域
- 活动区域
- 自定义

模板只是初始规则配置，管理员之后仍可逐项调整。

## 主领域点

每个 AdminRegion 支持命名领域点，1.4.0 GUI 主要提供 `primary` 主领域点：

- 管理员站在系统领域内部设置。
- 必须位于该领域范围中。
- 可以删除或重新设置。
- 管理员可直接传送到主领域点。
- 没有主领域点时，后台传送可回落区域中心。

底层按命名点设计，后续可以继续增加 `spawn / npc / exit / custom` 等点位而无需推翻数据结构。

## 自由进入 / 离开信息

管理员可以为每个系统领域独立配置：

- 进入 Title
- 进入 Subtitle
- 进入 ActionBar
- 进入聊天提示
- 离开 Title
- 离开 Subtitle
- 离开 ActionBar
- 离开聊天提示
- 每个通道单独开启/关闭
- Title fadeIn / stay / fadeOut

支持变量：

```text
%player%
%region%
%region_key%
%world%
%priority%
%type%
```

保留服务器已有的 `§#RRGGBB文字` RGB 语法，不做改写。

示例：

```text
进入 Title:
§#73E6A7翡翠森林

进入 Subtitle:
§#DCE8F5王国北部 · 高级资源区域

进入 ActionBar:
§#A8B8CA当前位置 §#73E6A7%region% §#7F8FA3| §#FFFFFF请遵守区域规则
```

领域进出跟踪只在“最高优先级系统领域发生变化”时触发，不会玩家每走一格重复刷提示。

## 管理员 GUI

系统领域后台提供：

- 系统领域列表
- 搜索
- 创建草稿
- 名称 / 内部 ID / 描述
- 优先级
- 用途模板
- 三态规则管理
- 玩家私人圈地规则
- 显示边界
- 主领域点
- 自定义进入/离开信息
- 调整范围
- 传送
- 删除

创建前可以先调整优先级，避免因为默认优先级与现有系统领域重叠而陷入死路。

创建系统领域覆盖现有玩家私人领地时，确认页会明确显示重叠数量并提示“系统显式规则优先”，不会静默覆盖。

## 玩家领地原有功能

- `/land` GUI：自有领地 + 已加入领地
- Owner / ADMIN / MEMBER / VISITOR / PUBLIC
- 权限模板
- 临时成员
- 黑名单
- Home / GUI传送
- 重命名、调整、转让、删除、日志
- Vault 永久额度
- 世界+Chunk空间索引
- FakePlayer、自动库存、漏斗/矿车漏斗、发射器/投掷器、非玩家改方块、爆炸、火焰、液体、活塞等保护
- 教程取消 / 完成后重新学习

## API

`YXLandAPI` 在 1.4.0 扩展 AdminRegion 查询能力，其他插件可以：

- 获取当前位置最高优先级系统领域
- 按内部 ID 获取系统领域
- 获取领域点
- 解析系统领域三态规则

可用于任务、NPC、传送、地图导航、YXClientEngine HUD 等后续系统联动。

## 安装

1. Java 8 + Minecraft Java Edition 1.12.2 服务端。
2. 将 `YXLand-1.4.0.jar` 放入 `plugins/`。
3. 推荐安装 Vault + 经济实现，用于玩家扩建/购买额度。
4. 设置 `config.yml -> worlds.enabled`。
5. `/land reload`。

## 权限

- `yxland.use`
- `yxland.create`
- `yxland.admin`
- `yxland.admin.region`
- `yxland.reload`
- `yxland.bypass`
- `yxland.group.vip`
- `yxland.group.svip`

`yxland.admin` 默认包含系统领域管理能力。

## 配置与存储

1.4.0 `config-version: 8`。系统领域与玩家领地一起进入现有快照/Dirty/单写锁/关服屏障持久化链，避免另起一套不安全 IO。

AdminRegion 持久化范围、优先级、用途类型、三态规则、领域点、进入/离开展示配置与 Title 时间参数。

## 性能

- 玩家 Land 与 AdminRegion 都使用 World + Chunk 候选索引。
- 高频保护事件不遍历全部系统领域。
- 三态解析只处理当前位置候选领域并按优先级排序。
- 进出提示只在跨方块/领域实际变化时处理。
- 边界显示继续使用统一 Scheduler。
- 数据保存使用脱离运行对象的快照与版本竞争保护。

## 构建与验证

生产依赖：`org.spigotmc:spigot-api:1.12.2-R0.1-SNAPSHOT`，Java source/target 1.8。

```bash
mvn clean package
```

离线验证：

```bash
./test.sh
./build.sh
```

1.4.0 最终交付态执行 **35 / 35** 自动测试通过，Java class major 52，JAR 中无 Bukkit/Bungee compile-stubs。详细验证见 `TEST_REPORT.md`。

当前环境没有用户实际 CatServer 1.12.2 + 全套模组客户端，因此自动测试和离线编译不能代替最终真实服测试。
