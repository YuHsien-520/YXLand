# YXLand 1.3.0 交付验证报告

验证日期：2026-08-09  
目标：Minecraft Java Edition 1.12.2 / Java 8

## 1.3.0 变更范围

### 教程生命周期

- 教程支持主动取消 `/land tutorial cancel`。
- 取消进入终态 `CANCELLED`，不会在以后 `/land` 时自动复活。
- 不实现暂停/继续。
- TutorialService 本身也禁止从 CANCELLED 直接 restart，避免以后其他模块误调用复活教程。
- 只有 `COMPLETE` 状态允许从第一步重新学习。
- CANCELLED / COMPLETE 都持久化到 `data.yml`。

### 持续火焰领地边界

- 边界效果统一切换为 `Effect.MOBSPAWNER_FLAMES`。
- 创建成功自动持续显示新领地。
- `/land show` / GUI 按钮切换持续显示。
- 不再使用 30 秒自动过期；旧 `duration-seconds` 仅保留配置兼容。
- 同一玩家同一时间只维护一个正式领地显示会话。
- 玩家下线清理，不跨登录持久化显示状态。
- 边界使用密集边线 + 四角/四边中点高火焰柱，并由最大采样点限制保护性能。

### 确认前持续显示候选范围

- 第一、第二点选择完成后，候选范围仍存在于 visualization session。
- 创建/扩建确认 GUI 打开期间继续渲染固定候选火焰边界。
- 点击创建取消会显式清空 SelectionManager，候选火焰立即停止。
- 确认成功无缝切换成正式领地持续显示。

### 扩建/缩小交互重做

- 新增独立“调整领地范围”信息页。
- 展示旧尺寸、面积、坐标、额度、剩余额度、价格规则和三步操作说明。
- 编辑期间：原范围使用稀疏/低火焰边框；新范围使用密集/高火焰边框。
- Title 实时显示原面积→新面积、增加/释放格数、费用、调整后额度和冲突原因。
- 第二点完成后打开详细确认 GUI，显示旧/新范围、价格、永久额度增加、Y=0~255、冲突/间距/尺寸校验。
- 支持重新选点和完全取消。

### 扩建经济与永久额度

固定规则：

- 普通玩家基础免费额度：70 XZ 格。
- 扩建每净新增 1 格：1000 Vault 金币。
- 缩小：0 金币，不退款。
- 每个成功付费新增格同时增加 1 格永久 purchased quota。
- 玩家用满 70/70 后扩到 71，只需在扩建确认时支付 1000；不再需要先买额度再重复付扩建费。
- 缩小不移除已购额度，释放出来的额度可用于其他领地。
- 手动额度商店默认同步为 1 格 / 1000 金币，GUI 提供 +1/+5/+10 格，避免旧版低价额度绕过扩建价格。
- 从旧 config-version 升级时，只有仍保持旧默认 `1000格/1000金币` 的额度商店会自动迁移；自定义值保留。

### 扩建交易安全

最终确认时重新计算/校验：

1. 新旧面积与新增格数
2. 最新费用
3. 世界、最小尺寸、单领地上限
4. 重叠和最小间距
5. 将本次付费新增格计入调整后永久额度
6. Vault 可用性与余额

付款成功后：

- 永久增加 purchased quota
- 更新边界/Chunk 索引
- 写审计日志
- Dirty 标记
- 因发生外部 Vault 交易，额外立即触发异步持久化快照
- 清除编辑状态
- 持续显示新边界

若付款后边界应用抛出 RuntimeException：

- purchased quota 恢复到交易前值
- 尝试 Vault 原额退款
- 不把该次编辑标记为成功

## 自动测试

执行：

```text
./test.sh
```

当前 Harness 共 **22 项**：

1. LandBoundsTest
2. LandPermissionTest
3. LandManagerTest
4. QuotaServiceTest
5. LandCodecTest
6. SelectionManagerTest
7. ProtectionServiceTest
8. FakePlayerClassifierTest
9. BoundarySamplerTest
10. BoundarySessionRegistryTest
11. SelectionPreviewServiceTest
12. QuotaPurchaseCalculatorTest
13. ResizePriceCalculatorTest
14. ResizeCapacityCalculatorTest
15. GuiContextTest
16. SaveVersionTrackerTest
17. LandSearchServiceTest
18. TutorialServiceTest
19. LandTransitionTrackerTest
20. PermissionTemplateTest
21. TemporaryGrantTest
22. TemporaryGrantDurationTest

新增 1.3.0 重点覆盖：

- persistent boundary session 不依赖到期时间
- 完成选择后仍属于 visualization session
- 取消/清理 selection 会停止候选显示所依赖的状态
- 扩建每新增格费用计算
- 70/70 → 71 的付费扩建容量计算
- 每个扩建新增格同步增加永久额度
- 缩小时永久额度不减少
- 多领地占用下的扩建额度计算
- 教程 CANCELLED 不可 restart
- COMPLETE 可 restart
- CANCELLED/COMPLETE 存储 round-trip

## 构建与结构验证

最终交付前重新执行：

```text
./test.sh
./build.sh
```

并检查：

- Java 主类 `major version: 52`（Java 8）
- JAR 不包含 `org/bukkit/` compile-stubs
- `plugin.yml` / `config.yml` / `messages.yml` 可正常 YAML 解析
- `pom.xml` 可正常 XML 解析
- 生产源码无 TODO / FIXME / TBD 占位实现
- 版本号统一为 1.3.0
- `config-version: 5`
- 源码 ZIP 可正常解压
- JAR / source ZIP 生成 SHA256

## API 与真实服务器验证边界

项目 `pom.xml` 指向 Spigot API `1.12.2-R0.1-SNAPSHOT`。当前沙箱没有 Maven，也无法从容器网络下载正式 API JAR，因此本地离线构建使用项目内针对 1.12.2 调用签名的 `compile-stubs`；这些 stub 会在构建后检查，确保不进入最终插件 JAR。

当前环境没有实际可启动并多人进入的 Spigot/Paper/CatServer 1.12.2 服务端，因此本报告不宣称真实 CatServer 联机测试完成。模组机器是否能被通用层拦截仍取决于混合端是否向 Bukkit 侧派发对应事件；完全绕过 Bukkit 事件的 Forge 机器需要针对具体模组追加 Hook。

## 最终本轮验证结果

本轮最终验证实际结果：

- `./test.sh`：22 / 22 PASS
- `./build.sh`：成功生成 `dist/YXLand-1.3.0.jar`
- 主类字节码：major version 52
- JAR 中 `org/bukkit/` 条目：0
- `plugin.yml`：解析通过
- `config.yml`：解析通过
- `messages.yml`：解析通过
- `pom.xml`：解析通过
- 生产源码 TODO / FIXME / TBD：0

最终源码 ZIP 与 SHA256 在交付阶段生成后再执行 ZIP 完整性检查。
