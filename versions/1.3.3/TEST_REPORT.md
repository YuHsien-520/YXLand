# YXLand 1.3.3 交付验证报告

验证日期：2026-08-09  
目标环境：Minecraft Java Edition 1.12.2 / Java 8

## 本版改动

### 1. 框选范围只来自真实 A/B 两点

- 只选择 A 点时不再使用玩家当前位置生成临时矩形。
- 玩家移动不会改变候选领地范围。
- 只有 A/B 两点都真实选择后，才渲染绿色贴地细线边界。
- 普通左键可重选 A，普通右键可重选 B，边界随真实点更新。

### 2. 手动确认手势

创建与扩建统一为：

```text
手持 YXLand 圈地工具 + 蹲下 + 右键
```

只有在 A/B 已完整锁定时才会打开确认 GUI。第二点那一次右键只负责锁定 B，不会同一次点击自动弹 GUI。右键空气或右键方块均可作为最终确认手势。

### 3. 动作信息栏

两点锁定后，不再使用屏幕中央 Title。物品栏上方 ActionBar 持续显示：

- 长×宽与 XZ 平面面积
- 可创建 / 冲突 / 超额等状态
- 扩建新增格数与金币费用
- `蹲下+右键` 打开创建/调整界面的提示

管理员无限额度仍显示为“管理员模式”，不会泄漏 Long.MAX_VALUE 数字。

## 自动测试

执行：

```text
./test.sh
```

最终结果：**27 / 27 PASS**。

新增覆盖：

- `SelectionConfirmGestureTest`：确认手势必须满足工具、蹲下、右键、完整两点。
- `SelectionActionBarFormatterTest`：动作信息栏只显示锁定 A/B 范围与简洁确认提示。
- `SelectionManagerTest`：A 点单独存在时不允许出现玩家位置矩形。
- `PreviewHudStyleTest`：Selection Preview 不再使用 Title，也不再调用玩家当前位置预览。

## 构建与静态验证

最终交付态已验证：

- `./test.sh`：27 / 27 PASS
- `./build.sh`：成功生成 `dist/YXLand-1.3.3.jar`
- Java 8 / class major 52
- JAR 内无 `org/bukkit` 或 `net/md_5` compile-stubs
- `plugin.yml` / `config.yml` / `messages.yml` / `pom.xml` 可解析
- 生产源码无 TODO/FIXME/TBD 占位
- Selection Preview 生产代码中无 `previewBounds(...)` 玩家位置临时范围逻辑

## 真实服务器验证边界

当前执行环境没有用户实际的 CatServer 1.12.2 + 客户端组合，因此最终交互手感仍建议在真实服务器测试一次；自动测试和编译验证用于保证逻辑与兼容性基础。
