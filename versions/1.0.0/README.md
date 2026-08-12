# YXLand 1.0.0

YXLand 是面向 Minecraft Java Edition 1.12.2 的永久领地保护与 GUI 管理插件，重点适用于资源世界、生存世界、玩家基地、矿区、农场与模组机器区域。

## 核心特性

- 永久领地，不包含自动过期或世界重置清理。
- 两点式 XZ 圈地，默认从 Y=0 保护到 Y=255。
- 世界 + Chunk 空间索引，保护事件不全量扫描所有领地。
- 玩家专属 `/land` 管理 GUI：自有领地 + 已加入领地、信息、显示边界、成员、角色权限、访问/环境权限、Home、传送、重命名、调整范围、转让、删除、日志。
- 玩家点击 GUI 中“显示领地边界”后，边界只发送给该玩家并自动结束。
- 基础免费面积额度 + Vault 金币购买永久额外额度 + 权限组额度。
- 领地数量、总面积、单块最大面积、最小边长、领地间距均可配置。
- Owner / ADMIN / MEMBER / VISITOR / PUBLIC 权限模型。
- 黑名单优先，支持禁止陌生玩家进入领地。
- 保护方块、容器、常见交互、桶、红石、实体、PVP、爆炸、火焰、液体、活塞、悬挂实体、多方块放置、玩家踩踏类方块变化与跨边界移动。
- 对模组机器使用 Bukkit/混合端暴露的方块交互和 InventoryOpen 事件进行保护。
- Dirty 标记 + 批量异步保存；版本号阻止旧异步快照覆盖新数据；关闭时使用写入屏障执行最终同步保存；临时文件 + 原子替换。
- 数据加载失败时停止插件并禁止空数据覆盖原领地数据。
- Vault 通过反射 soft-hook；没有 Vault 时核心领地保护照常工作，仅额度购买不可用。
- 所有玩家可见文本保留 `§#RRGGBB` 语法，由服务器现有客户端模组负责渲染。

## 安装

1. 使用 Java 8 兼容的 Minecraft 1.12.2 服务端（Spigot/PaperSpigot；混合端需正确转发 Bukkit 事件）。
2. 将 `YXLand-1.0.0.jar` 放入 `plugins/`。
3. 可选：安装 Vault 和一个 Vault 经济实现，用于购买额外领地额度。
4. 启动服务器生成 `plugins/YXLand/config.yml` 和 `messages.yml`。
5. 修改 `worlds.enabled`，填入允许玩家圈地的实际世界名称，然后 `/land reload`。

默认配置只启用名为 `resource` 的世界；如果你的资源世界名称不同，必须修改该列表。

## 玩家流程

1. `/land` 打开“我的领地”。
2. 点击“创建新领地”获得 YXLand 圈地工具。
3. 左键方块选择 A 点，右键方块选择 B 点。
4. 系统按 XZ 生成矩形领地并打开创建确认 GUI。
5. 确认页会检查面积额度、单块上限、数量上限、重叠和最小间距。
6. 创建后在 `/land` 中管理该领地。

## 领地管理 GUI

- **领地信息**：名称、世界、坐标、面积、成员等。
- **显示领地边界**：按需显示，默认 30 秒，仅当前玩家可见。
- **成员管理**：添加成员、切换 ADMIN/MEMBER/VISITOR、移除成员。
- **角色权限**：破坏、放置、容器、交互、红石、桶、PVP、生物伤害、进入等。
- **访问/环境**：PUBLIC 进入、爆炸、火焰、液体、活塞、黑名单。
- **传送/Home**：设置 Home 后从 GUI 或命令传送。
- **重命名**：通过聊天输入新名称。
- **调整边界**：进入专用重新选点模式，再二次确认。
- **转让**：输入在线目标玩家并检查对方数量/面积上限，再二次确认。
- **删除**：危险操作二次确认。
- **操作日志**：记录领地关键管理变更。
- **成员可见性**：被邀请的成员会在自己的 `/land` 列表看到加入的领地，并按角色权限进入管理中心。
- **管理员搜索**：后台可按领地名、主人名、领地/主人 UUID 前缀检索。

## 指令

- `/land` — 打开玩家领地 GUI
- `/land help` — 指令帮助
- `/land wand` / `/land create` — 获取圈地工具
- `/land tp <领地>` — 传送到自己的领地
- `/land sethome <领地>` — 设置领地 Home
- `/land show <领地>` — 显示领地范围
- `/land buy` — 打开额度商店
- `/land admin` — 管理员 GUI
- `/land reload` — 安全重载配置
- `/land save` — 立即保存
- `/land debug` — 查看运行状态

## 权限

- `yxland.use` — 基础使用，默认 true
- `yxland.create` — 创建领地，默认 true
- `yxland.admin` — 管理员功能，默认 OP
- `yxland.reload` — 重载，默认 OP
- `yxland.bypass` — 绕过保护，默认 OP
- `yxland.group.vip` — VIP 额度组
- `yxland.group.svip` — SVIP 额度组

权限组可在 `config.yml -> limits.groups` 自定义并通过 priority 选择最高优先级匹配项。

## 默认额度

默认普通玩家：

- 最多 3 个领地
- 10,000 格总基础面积
- 单块最多 50,000 格
- 最小 4×4
- 不同领地之间至少 3 格空隙
- 火焰蔓延默认关闭；液体与活塞可在领地内部工作，但不能跨越领地边界
- 单块领地最多索引 16,384 个 Chunk（技术安全上限，防止异常超大范围拖垮服务器）

默认额度商店每份增加 1,000 格永久额度，价格 1,000 Vault 金币。所有值均可配置。

## 数据

默认数据文件：`plugins/YXLand/data.yml`

保存内容包括：

- UUID 领地主人
- 世界与 XZ 边界
- 成员与角色
- 黑名单
- 角色 Flag
- 环境 Flag
- Home
- 操作日志
- 玩家永久购买面积

玩家数据均使用 UUID，不依赖玩家名称作为主键。

## 性能设计

- `findAt` 使用世界 + Chunk 候选集合，不遍历全服所有领地。
- 领地与额度常驻内存，保护事件不读 YAML。
- 自动保存先在主线程创建脱离运行对象的快照，再异步写文件；旧版本快照会在真正落盘前再次校验版本。
- 一个统一 BoundaryVisualizer 周期任务管理全部边界显示会话。
- 边界按步长采样并设置最大采样密度，不逐方块永久刷粒子。
- PlayerMoveEvent 仅在玩家 X/Z 方块或世界发生变化时处理。
- 领地索引存在 16,384 Chunk 的单领地技术保护上限，避免异常坐标或管理员误操作产生超大索引。
- 玩家退出会清理选择、聊天输入、边界会话和传送冷却缓存。

## 配置升级

启动和 `/land reload` 会将 JAR 中新增的默认配置节点补入现有 `config.yml`，并保留已有值。当前 `config-version: 1`。

## 构建

### 正常 Maven 构建

项目 `pom.xml` 使用：

- `org.spigotmc:spigot-api:1.12.2-R0.1-SNAPSHOT`
- Java source/target 1.8

有 Maven 和网络时：

```bash
mvn clean package
```

产物位于 `target/YXLand-1.0.0.jar`。

### 离线验证构建

仓库包含 `compile-stubs/`，只用于当前无 Maven/无网络环境下验证 Java 8 语法和 Bukkit API 调用结构：

```bash
./test.sh
./build.sh
```

`compile-stubs` **不会打进插件 JAR**。正常生产构建仍建议使用 Maven + 实际 Spigot 1.12.2 API 再做一次编译。

当前交付前离线测试 Harness 共执行 12 个核心回归测试，覆盖几何、权限、索引、额度、序列化、选择、保护决策、边界采样、额度购买、GUI 路由、保存版本竞争和管理员搜索。

## 已知限制

- 模组机器能否被 Bukkit 事件拦截，取决于 CatServer/其他混合端是否把对应模组交互转发为 Bukkit 的 PlayerInteractEvent / InventoryOpenEvent。纯 Forge 绕过 Bukkit 事件的特殊机器，需要针对具体模组增加 Hook。
- 当前默认持久化为 YAML。代码通过 Repository 接口隔离，后续可增加 SQLite/MySQL 后端，但 1.0.0 未内置数据库驱动。
- `§#RRGGBB` 为服务器现有模组提供的自定义显示能力，YXLand 原样保留字符串。

## 目录

- `src/main/java` — 插件源码
- `src/main/resources` — plugin.yml/config.yml/messages.yml
- `src/test/java` — 无第三方依赖的核心逻辑测试
- `compile-stubs` — 仅离线静态编译验证
- `docs/superpowers` — 设计与实施规格
