# YXLand 1.3.1 交付验证报告

验证日期：2026-08-09  
目标：Minecraft Java Edition 1.12.2 / Java 8

## 1.3.1 变更范围

### 边界视觉根因修复

1.3.0 的边界同时叠加多层水平火焰线、四角高柱、四边中点柱，火焰粒子本身体积又大，导致近距离观察时画面被大量粒子遮挡，无法清楚读出矩形范围。

1.3.1 改为用户确认的“方案2”：

- `Effect.HAPPY_VILLAGER` 绿色小粒子
- 只绘制 XZ 最外围四条边
- 单层水平细线
- 不填充内部
- 不生成任何竖柱/中点柱
- 四角只在同一水平面沿相邻两边短距离加密
- 小范围使用亚方块采样，超大范围受 max-edge-points 自适应限制

### 完全水平固定 Y

- 新建/扩建第一点记录 `clickedBlockY + 1.05` 作为本次预览固定 Y。
- 第二点不会改变固定 Y。
- 确认 GUI 打开期间继续使用同一个 Y。
- 正式 `/land show` / GUI 显示会话记录开启时玩家所在 Y。
- 玩家之后跳跃、上下移动不会让该显示会话的边界跟随变化。
- 扩建旧范围与新候选范围共用同一水平面。

### 扩建双范围视觉

- 旧范围：同色绿色细线，但更稀疏、无角点强化。
- 新范围：更密的绿色细线 + 轻微四角强化。
- 不再通过“高柱/高火焰”区分新旧范围，避免重新产生遮挡。

### 其他规则保持

- 普通玩家基础免费额度：70 XZ 格。
- Y=0~255 全高度永久保护，Y 不计额度/费用。
- 扩建每净新增 1 格：1000 Vault 金币，并同步永久增加 1 格 purchased quota。
- 缩小：0 金币，不退款。
- 教程只支持取消；完整完成后才支持重新学习。
- FakePlayer、自动库存、发射器、非玩家改方块等保护逻辑不变。

## 自动测试

执行：

```text
./test.sh
```

1.3.1 Harness 共 **24 项**：

1. LandBoundsTest
2. LandPermissionTest
3. LandManagerTest
4. QuotaServiceTest
5. LandCodecTest
6. SelectionManagerTest
7. ProtectionServiceTest
8. FakePlayerClassifierTest
9. BoundarySamplerTest
10. CornerAccentSamplerTest
11. BoundaryVisualStyleTest
12. BoundarySessionRegistryTest
13. SelectionPreviewServiceTest
14. QuotaPurchaseCalculatorTest
15. ResizePriceCalculatorTest
16. ResizeCapacityCalculatorTest
17. GuiContextTest
18. SaveVersionTrackerTest
19. LandSearchServiceTest
20. TutorialServiceTest
21. LandTransitionTrackerTest
22. PermissionTemplateTest
23. TemporaryGrantTest
24. TemporaryGrantDurationTest

1.3.1 新增/强化覆盖：

- 0.5 等亚方块间距的外围采样
- 所有基础采样点只能出现在矩形四条外边
- block-edge 四角闭合
- 超大范围采样上限
- 四角强化点只沿水平边界，不进入内部
- selection 第一点击中后固定 Y
- 第二点不会改变固定 Y
- 正式边界显示会话保存固定 Y
- 切换显示领地时同步切换显示 Y
- 生产 BoundaryVisualizer 必须使用 HAPPY_VILLAGER
- 生产 BoundaryVisualizer 不得再出现 MOBSPAWNER_FLAMES / renderPillars / 多层边线 getter

## 构建与结构验证

最终交付前重新执行：

```text
./test.sh
./build.sh
```

并检查：

- Java 主类 major version 52（Java 8）
- JAR 不包含 `org/bukkit/` compile-stubs
- `plugin.yml` / `config.yml` / `messages.yml` YAML 可解析
- `pom.xml` XML 可解析
- 生产源码无 TODO / FIXME / TBD
- 版本号统一为 1.3.1
- `config-version: 6`
- 源码 ZIP 可完整解压
- JAR / source ZIP SHA256 生成并核对

## API 与真实服务器验证边界

`pom.xml` 仍指向 `org.spigotmc:spigot-api:1.12.2-R0.1-SNAPSHOT`。当前容器网络无法下载正式 Spigot API JAR，因此本地离线构建继续使用项目内 1.12.2 调用签名 compile-stubs；这些 stub 有独立 JAR 内容检查，禁止进入最终插件 JAR。

当前环境没有实际可启动并多人进入的 Spigot/Paper/CatServer 1.12.2 服务端，因此本报告不会把离线验证描述成真实 CatServer 联机测试。

## 最终本轮验证结果

最终交付态重新执行结果：

- `./test.sh`：**24 / 24 PASS**
- `./build.sh`：成功生成 `dist/YXLand-1.3.1.jar`
- `YXLandPlugin.class`：**major version 52 / Java 8**
- `BoundaryVisualizer.class` 常量池：包含 `Effect.HAPPY_VILLAGER`，不包含 `MOBSPAWNER_FLAMES`
- JAR 中 `org/bukkit/` 条目：**0**
- `plugin.yml`：YAML 解析通过
- `config.yml`：YAML 解析通过
- `messages.yml`：YAML 解析通过
- `pom.xml`：XML 解析通过
- 生产源码 TODO / FIXME / TBD：**0**
- 生产 `BoundaryVisualizer`：无 `renderPillars`、无多层边线 getter、无火焰粒子调用

源码 ZIP 与 SHA256 在打包后继续做完整性校验。
