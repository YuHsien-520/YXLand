# YXLand 1.3.2

YXLand 是面向 Minecraft Java Edition 1.12.2 的永久领地保护与 GUI 管理插件，重点适用于资源世界、生存世界、玩家基地、矿区、农场与模组机器区域。

## 1.3.2 核心规则

- 领地只按 X×Z 平面计算；Y 不消耗额度、不参与扩建费用，创建后 Y=0~255 全高度永久保护。
- 普通玩家默认基础永久额度 70 格，VIP/SVIP 默认示例为 140/280。
- 扩建每新增 1 格默认 1000 金币，成功后同步永久增加 1 格 purchased quota；缩小免费、不退款。

## 1.3.2 视觉修正

### 绿色贴地细线边界

1.3.2 保留方案2：**单层绿色细线 + 四角轻微强化**，但边界高度改为**跟随地表起伏**。

正式领地、新建预览和扩建候选范围统一使用 `HAPPY_VILLAGER` 绿色小粒子：

- 只绘制 XZ 矩形最外围四条边
- 不填充内部
- 不生成竖向粒子柱、中点柱或多层边线
- 小/中型领地使用亚方块间距采样
- 四角只沿相邻两条边短距离加密
- 每个边界点根据对应领地内侧方块的地表高度显示
- far edge 高度采样夹回领地内侧方块，避免误跟随隔壁地形
- 粒子只发送给当前查看玩家

边界不再保存固定 Y；每次渲染都按地表高度绘制。

### HUD 超长数字修复

管理员无限额度内部使用 `Long.MAX_VALUE`，1.3.1 可能把 `9223372036854775807` 直接显示到预览 HUD。1.3.2 改为：

- 管理员创建预览：`可创建 | 管理员模式`
- 普通玩家：`可创建 | 剩余 N 格`
- 额度不足：`超出 N 格`
- 不再输出内部无限额度哨兵，也不再拼接冗长 `已用+面积/总额度` 表达式

## 新手教程与创建流程

教程仍只保留“取消”和“完成后重新学习”：`/land tutorial cancel` 会进入 CANCELLED 终态，不暂停/继续；只有完整完成教程的玩家才能 `/land tutorial` 从头重学。

创建流程仍为两点 XZ 选择；候选范围在确认 GUI 打开期间持续显示，取消后清除，确认成功后无缝切换为正式持续绿色贴地边界。

## 扩建流程

管理中心 → **调整领地范围** 会先显示当前尺寸、XZ 坐标、面积、额度、剩余额度、单格价格、缩小规则和操作说明。编辑时：

- 旧范围使用较稀疏绿色贴地细线
- 新范围使用更密绿色贴地细线 + 四角轻强化
- 实时显示旧面积→新面积、增加/释放格数、费用、调整后额度和冲突原因
- 第二点完成后仍保留候选边界，并进入最终确认页

最终确认会重新校验范围、Vault 和余额，再扣款、增加永久额度、更新 Chunk 索引、写审计日志并持久化；异常时恢复额度并尝试退款。

## 其他核心功能

永久领地、玩家 `/land` GUI、Owner/ADMIN/MEMBER/VISITOR/PUBLIC 权限、权限模板、临时成员、黑名单、Home/传送、重命名、转让、删除、操作日志、进入/离开提示、Vault 额度购买、管理员搜索、World+Chunk 空间索引、FakePlayer、自动库存/漏斗/发射器、非玩家改方块、爆炸/火焰/液体/活塞等保护保持不变。

## 安装

1. Java 8 + Minecraft 1.12.2 服务端。
2. 将 `YXLand-1.3.2.jar` 放入 `plugins/`。
3. 推荐安装 Vault + 经济插件。
4. 配置 `worlds.enabled` 后 `/land reload`。

主要指令：`/land`、`/land wand`、`/land create`、`/land show <领地>`、`/land tp <领地>`、`/land sethome <领地>`、`/land buy`、`/land tutorial`、`/land tutorial cancel`、`/land admin`、`/land reload`、`/land save`、`/land debug`。

## 默认权限

`yxland.use`、`yxland.create`、`yxland.admin`、`yxland.reload`、`yxland.bypass`、`yxland.group.vip`、`yxland.group.svip`。

## 关键配置

```yaml
config-version: 6
limits:
  default:
    max-lands: 3
    base-area: 70
    max-single-area: 50000
quota-shop:
  unit-area: 1
  unit-price: 1000.0
resize:
  price-per-added-block: 1000.0
boundary:
  persistent-until-disabled: true
  refresh-ticks: 10
  line-spacing: 0.45
  max-edge-points: 480
  corner-accent:
    enabled: true
    length: 0.80
    spacing: 0.15
selection-preview:
  enabled: true
  refresh-ticks: 8
  line-spacing: 0.35
  max-edge-points: 600
  corner-accent:
    enabled: true
    length: 0.90
    spacing: 0.12
  resize-original-line-spacing: 0.90
  resize-original-max-points: 300
  show-title: true
```

## 数据与性能

数据保存在 `plugins/YXLand/data.yml`，玩家主键使用 UUID。保护查询使用 World+Chunk 空间索引；单领地最多索引 16,384 Chunk；边界/圈地/扩建预览共用统一 Scheduler；绿色细线有 `max-edge-points` 限制；保存采用 Dirty + 异步快照 + 版本竞争保护 + 关闭写入屏障。

## 构建与验证

`pom.xml` 使用 `org.spigotmc:spigot-api:1.12.2-R0.1-SNAPSHOT`，Java source/target 1.8。

```bash
mvn clean package
# 或离线验证
./test.sh
./build.sh
```

1.3.2 交付时 Harness 共 **25 项自动回归测试**。当前交付环境没有用户实际 CatServer/客户端组合，因此不宣称真实联机测试完成。详细验证见本目录 `TEST_REPORT.md`。
