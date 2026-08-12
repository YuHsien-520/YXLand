# YXLand 1.4.0 交付验证报告

验证日期：2026-08-10  
目标环境：Minecraft Java Edition 1.12.2 / Java 8

## 1.4.0 主要新增

### 独立 AdminRegion 系统领域

- 玩家 `Land` 与管理员 `AdminRegion` 使用独立模型、独立 ID、独立空间索引与独立管理员选区。
- 系统领域不消耗玩家70格额度、不计玩家领地数量、不收取 Vault 金币。
- 系统领域可不同优先级重叠；同优先级发生范围重叠时拒绝创建/调整。
- 范围索引仍使用 World + Chunk 候选桶，不在高频保护事件中遍历全部系统领域。

### 三态优先级解析

规则使用 `INHERIT / ALLOW / DENY`：

- 高优先级显式 ALLOW/DENY 优先。
- 高优先级 INHERIT 会继续查低优先级系统领域。
- 全部 INHERIT 后回落玩家领地/野外规则。
- `PLAYER_CLAIM` 使用相同解析模型，并对待圈矩形做精确分区检查，允许高优先级子区域覆盖低优先级大区域的私人圈地规则。

### 管理员 GUI 与领域点

- `/land admin → 系统领域` 与 `/land admin region`。
- 独立管理员领域工具：真实 A/B 两点 + 蹲下右键手动确认。
- 列表、搜索、创建草稿、优先级、用途模板、三态规则、范围调整、删除。
- `primary` 主领域点设置、删除、传送；必须位于领域范围内。
- 创建系统领域覆盖玩家私人领地时，确认页明确显示重叠数量与系统规则优先警告。

### 自由进入/离开展示

支持管理员自定义：

- enter/exit Title + Subtitle
- enter/exit ActionBar
- enter/exit Chat
- 各通道开关
- Title fadeIn/stay/fadeOut
- `%player% / %region% / %region_key% / %world% / %priority% / %type%`
- 保留 `§#RRGGBB` 文本原样

位置切换只以最高优先级系统领域变化为触发条件，不会每移动一个方块重复刷提示。

### 模组服保护融合

系统领域三态规则已进入玩家操作、进入限制、FakePlayer、爆炸、火焰、液体、活塞、自动库存/机器等现有保护链。INHERIT 时保持原玩家领地保护逻辑。

## 自动测试

最终交付前运行：

```text
./test.sh
```

当前测试集：**35 项**。

新增覆盖包括：

- `AdminRegionTest`
- `AdminRegionManagerTest`
- `AdminRegionDraftManagerTest`
- `AdminRegionResolverTest`
- `AdminRegionTransitionTrackerTest`
- `AdminRegionCodecTest`
- `AdminRegionSelectionManagerTest`
- `RegionMessageFormatterTest`
- `GuiContextTest` 的系统领域槽位绑定

重点验证：

- 不同优先级可重叠
- 同优先级重叠拒绝
- 高优先级 ALLOW/DENY
- INHERIT 向下解析
- PLAYER_CLAIM 高优先级子区域覆盖
- 全字段序列化/反序列化
- 展示占位符替换不破坏 RGB
- 领域进出切换去重
- 玩家选区与管理员选区隔离

## 构建与静态验证

使用项目离线 Java 8 编译链：

```text
./build.sh
```

该路径使用签名兼容的 1.12.2 compile-stubs 编译，stubs 不会打入 JAR。

最终交付态已执行并通过：

- `./test.sh`：35 / 35 PASS
- `./build.sh`：生成 `dist/YXLand-1.4.0.jar`
- Java 8：class major 52
- JAR 内 `org/bukkit` / `net/md_5` compile-stub 泄漏：0
- `plugin.yml / config.yml / messages.yml` YAML 解析：通过
- `pom.xml` XML 解析：通过
- `plugin.yml` 版本：1.4.0
- `config-version`：8
- TODO/FIXME/TBD 生产源码扫描：0
- 管理员权限、GUI、管理员工具监听、API规则解析、展示编辑输入入口静态检查：通过

源码 ZIP 完整性与 SHA256 在最终打包后单独复核。

## 真实服务器验证边界

当前执行环境没有用户实际 CatServer 1.12.2 + 全套模组客户端。因此自动测试、离线编译和静态 API 兼容检查不能替代真实服的最终交互测试。尤其建议实机验证：

- Forge 模组中完全不触发 Bukkit 事件的特殊机器
- Title/ActionBar 在用户自定义客户端 RGB 渲染链中的实际显示
- 大型重叠系统领域下的粒子与移动体验
