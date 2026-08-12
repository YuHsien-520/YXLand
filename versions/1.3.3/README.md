# YXLand 1.3.3

Minecraft Java Edition **1.12.2** 永久领地保护与 GUI 管理插件。

## 1.3.3 关键交互改动

### 框选范围只认真实 A/B 两点

- 左键选择 A 点后，只记录 A，不再拿玩家当前位置充当临时 B 点。
- 玩家移动不会改变候选范围，也不会产生“跟着玩家跑”的假矩形。
- 右键真正选择 B 点后，才形成 A↔B 的 XZ 矩形并显示绿色贴地细线。
- 普通左键可以重新选择 A，普通右键可以重新选择 B，范围只随真实 A/B 更新。

### 选完后不自动弹确认 GUI

A/B 完成后仍留在世界中观察自己框好的区域。物品栏上方 ActionBar 持续显示面积、状态和确认提示，而不是立即打开界面。

最终确认手势统一为：

```text
手持 YXLand 圈地工具 + 蹲下 + 右键
```

必须同时满足：

- 手里是 YXLand 圈地工具
- A/B 两点已经完整选择
- 玩家正在蹲下
- 发生右键动作

第二点那一次右键只负责锁定 B，不会同一次点击误弹确认界面；下一次蹲下右键才进入创建/扩建确认 GUI。右键空气或方块都可以作为最终确认动作。

创建和扩建流程统一使用这套规则。

## ActionBar 示例

普通创建：

```text
✓ 7×10=70格 | 剩余 0格 | 蹲下+右键 打开创建界面
```

扩建：

```text
调整 70→86格 | +16格 / 16000金币 | 蹲下+右键 打开调整界面
```

管理员无限额度显示“管理员模式”，不会输出 `Long.MAX_VALUE`。

## 其他核心规则

- 玩家领地额度只按 X×Z 计算，Y 不参与额度或扩建收费。
- 创建后 XZ 范围从 Y=0~255 全高度永久保护。
- 普通玩家默认基础额度 70 格。
- 扩建每净新增 1 格默认 1000 Vault 金币，并同步永久增加 1 格已购额度；缩小不收费、不退款。
- 绿色边界使用 `HAPPY_VILLAGER` 小粒子，只描矩形四边并贴地形起伏，不生成火焰墙、竖柱、多层线或内部填充。
- 教程支持取消；取消后不会自动恢复，只有完整学完后才能重新开始。
- 玩家 GUI、成员/角色权限、权限模板、临时成员、黑名单、Home、转让、删除、日志、Vault、FakePlayer、自动机器和环境保护均保留。

## 安装

1. 使用 Java 8 兼容的 Minecraft 1.12.2 服务端。
2. 将 `YXLand-1.3.3.jar` 放入 `plugins/`。
3. 推荐安装 Vault + 经济实现。
4. 设置 `config.yml -> worlds.enabled` 后执行 `/land reload`。

## 主要指令

`/land`、`/land wand`、`/land create`、`/land show <领地>`、`/land tp <领地>`、`/land sethome <领地>`、`/land buy`、`/land tutorial`、`/land tutorial cancel`、`/land admin`、`/land reload`、`/land save`、`/land debug`。

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

1.3.3 最终交付态执行 **27 / 27** 自动测试通过，Java class major 52，JAR 中无 Bukkit/Bungee compile-stubs。详细结果见 `TEST_REPORT.md`。

当前环境没有用户真实 CatServer 1.12.2 + 客户端组合，因此自动测试不能替代最终实机交互验证。
