# YXLand 1.2.0 交付验证报告

验证日期：2026-08-09  
目标：Minecraft Java Edition 1.12.2 / Java 8

## 本次版本内容

YXLand 1.2.0 在 1.1.0 的永久 XZ 全高度领地基础上新增五个正式模块：

1. **高可视实时圈地预览**
   - 选择第一点后立即启用。
   - 默认边线每 1 格一个粒子，并叠加 2 个水平层。
   - 四角 + 四边中点显示高亮竖柱。
   - 屏幕中央实时显示 `长 × 宽 = XZ面积`、已使用/总额度、创建后剩余额度、冲突与超限原因。
   - 大范围由 `max-edge-points` 自动限制采样量，防止无限粒子。
   - 第二点确认或选择取消后停止预览。

2. **进入/离开领地提示**
   - 进入显示领地名、主人、XZ面积。
   - 离开显示回到野外。
   - 从一块领地直接进入另一块领地使用切换提示。
   - PlayerMoveEvent 仅在 X/Z 方块或世界实际变化时判断。

3. **权限模板**
   - 完全私人
   - 好友基地
   - 公共参观
   - 机器基地
   - GUI 应用前二次确认，防误覆盖现有自定义权限。

4. **模组服 / 自动化防绕过强化**
   - FakePlayer 默认拒绝，支持 extra-names / allowed-names。
   - FakePlayer 默认不继承 `yxland.bypass`。
   - 非玩家通过 EntityChangeBlockEvent 修改领地方块默认拒绝。
   - InventoryMoveItemEvent 自动库存转移跨边界阻断。
   - InventoryPickupItemEvent 漏斗/矿车漏斗跨边界吸取掉落物阻断。
   - BlockDispenseEvent 发射器/投掷器跨边界动作阻断。
   - 无法解析自动库存位置且另一侧处于受保护领地时，可配置为安全拒绝。

5. **临时成员授权**
   - MEMBER 临时角色：30分钟 / 1小时 / 3小时 / 12小时 / 1天。
   - 使用绝对到期时间戳，不为每个授权创建独立 Bukkit 定时任务。
   - 到期自动失效；服务器重启后仍按原到期时间判断。
   - 成员 GUI 显示临时角色和剩余时间。
   - 可提前撤销。
   - 已有更高永久角色不会被临时 MEMBER 降级。

原有核心规则保持不变：领地额度只计算 X×Z，Y 不计费；创建成功后 Y=0~255 全高度永久保护；普通玩家基础额度 70 格。

## 自动测试

执行：

```text
./test.sh
```

当前测试 Harness 共 **19 项**：

- LandBoundsTest
- LandPermissionTest
- LandManagerTest
- QuotaServiceTest
- LandCodecTest
- SelectionManagerTest
- ProtectionServiceTest
- FakePlayerClassifierTest
- BoundarySamplerTest
- SelectionPreviewServiceTest
- QuotaPurchaseCalculatorTest
- GuiContextTest
- SaveVersionTrackerTest
- LandSearchServiceTest
- TutorialServiceTest
- LandTransitionTrackerTest
- PermissionTemplateTest
- TemporaryGrantTest
- TemporaryGrantDurationTest

覆盖重点：

- XZ 几何、面积、重叠、最小间距、Chunk 覆盖与 Y=0~255 语义
- Owner/ADMIN/MEMBER/VISITOR/PUBLIC 与黑名单
- 70 格额度、总额度、单块面积与购买计算
- 两点选择及第一点后的实时预览范围/剩余额度/冲突状态
- 进入/离开/领地切换状态机
- 四种权限模板行为
- 临时角色生效、到期、永久高角色不降级、保存/恢复
- FakePlayer 判定
- 自动库存跨领地决策
- 保存版本竞争保护
- 管理员搜索与教程状态

## 构建验证

执行：

```text
./build.sh
```

预期产物：

```text
dist/YXLand-1.2.0.jar
```

交付前继续检查：

- Java 主类 major version = 52（Java 8）
- JAR 不包含 `org/bukkit/` compile-stubs
- plugin.yml / config.yml / messages.yml 均能被 YAML 解析
- pom.xml 可被 XML 解析
- 生产源码无 TODO / FIXME / TBD 占位实现
- 完整源码 ZIP 可正常解压并包含构建、资源、测试与源码目录

## 1.12.2 API 核对

本版新增 Bukkit 接入点主要为：

- `Player.sendTitle(String, String, int, int, int)`
- `InventoryMoveItemEvent`
- `InventoryPickupItemEvent`
- `BlockDispenseEvent`

这些接口均在 Spigot 1.12.x/1.12.2 API 文档中存在。当前沙箱无法直接联网下载官方 API JAR 执行第二套真实依赖编译，因此最终 JAR 的本地构建仍使用项目内的 1.12.2 签名编译桩；编译桩不会被打入插件 JAR。

## 运行时限制

当前环境没有一套可实际启动并多人进入的 Spigot/Paper/CatServer 1.12.2 服务器，所以本报告不宣称真实 CatServer 联机测试完成。

尤其是模组机器：只有混合端向 Bukkit 侧发出相应事件时，通用保护层才能拦截。完全绕过 Bukkit 事件的 Forge 机器仍需要针对具体模组追加 Hook。YXLand 已把这类行为集中到 `mod-protection` 配置与保护层中，后续可以继续扩展。
