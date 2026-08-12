# YXLand 1.3.2 交付验证报告

验证日期：2026-08-09  
目标环境：Minecraft Java Edition 1.12.2 / Java 8

## 本版修复

### 1. 绿色边界改为贴地形起伏

1.3.1 使用固定 Y 水平边框。1.3.2 按玩家反馈改为地表跟随：

- 仍然只绘制 XZ 矩形最外围四条细线。
- 仍使用 `Effect.HAPPY_VILLAGER` 绿色小粒子。
- 不恢复火焰、竖柱、中点柱、多层线或内部填充。
- 每个采样点按对应领地内侧方块的 `World#getHighestBlockYAt(x,z)` 求地表高度，然后在地表上方显示粒子。
- 最大 X/Z 边界在视觉坐标上位于 `max+1`，高度采样会夹回领地内部方块，避免边界高度错误取到隔壁地形。
- 单次渲染对相同 X/Z 方块高度做局部缓存，亚方块密集粒子不会重复查询同一地表高度。
- 删除 BoundaryVisualizer 的固定 Y 捕获逻辑；BoundarySessionRegistry 与 SelectionManager 也不再保存 visualY 状态。

### 2. 实时圈地 HUD 超长数字修复

截图中的超长数字来自管理员预览内部使用的 `Long.MAX_VALUE` 无限额度哨兵值（9223372036854775807）被直接拼进 Subtitle。

1.3.2 改为：

- 管理员创建预览：`可创建 | 管理员模式`。
- 普通玩家创建预览：`可创建 | 剩余 N 格`。
- 不再显示 `已用+本次面积/总额度` 的长表达式。
- 额度不足提示只显示 `超出 N 格`，不直接输出内部总额度哨兵。
- 扩建实时 HUD 同样对无限额度显示 `管理员模式`，不会输出 Long.MAX_VALUE。

## 自动测试

执行：

```text
./test.sh
```

最终结果：**25 / 25 PASS**。

本版新增 `PreviewHudStyleTest`，并强化 `BoundaryVisualStyleTest`：

- 生产 BoundaryVisualizer 必须使用绿色 `HAPPY_VILLAGER`。
- 不允许重新出现 `MOBSPAWNER_FLAMES`。
- 不允许出现竖柱和多层边线渲染。
- 必须使用 `getHighestBlockYAt` 做地形高度采样。
- BoundaryVisualizer 不得再包含 `captureDisplayY` 固定平面逻辑。
- 管理员预览必须使用短文本 `管理员模式`。
- 创建 HUD 不得重新拼接 `used + area / Long.MAX_VALUE` 长额度表达式。

## 构建与静态验证

最终交付态重新执行：

```text
./test.sh
./build.sh
```

验证结果：

- `./test.sh`：**25 / 25 PASS**
- `./build.sh`：成功生成 `dist/YXLand-1.3.2.jar`
- `YXLandPlugin.class`：**major version 52 / Java 8**
- JAR 内 `org/bukkit/` compile-stubs：**0**
- `plugin.yml`：YAML 解析通过
- `config.yml`：YAML 解析通过
- `messages.yml`：YAML 解析通过
- `pom.xml`：XML 解析通过
- 生产源码 `TODO / FIXME / TBD`：**0**
- 生产代码固定 Y 旧引用：**0**
- 实时预览旧 `used+area/total` 长表达式：**0**

## 真实服务器验证边界

当前执行环境没有用户实际使用的 CatServer/客户端组合，因此无法在这里对粒子最终视觉密度、材质包/客户端 HUD 缩放进行真实进服截图验证。本版对用户截图中可由源码确认的两个根因进行了代码级修复，并完成自动测试与构建验证。
