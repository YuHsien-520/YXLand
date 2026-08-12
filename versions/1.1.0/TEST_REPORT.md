# YXLand 1.1.0 交付验证报告

验证日期：2026-08-09
目标：Minecraft Java Edition 1.12.2 / Java 8

## 本次修改重点

- 领地额度正式定义为 **XZ 水平平面范围**，公式为 `width × depth`。
- Y 坐标不参与额度计算，领地固定保护 Y=0~255。
- 普通玩家默认基础额度调整为 **70 格**。
- 1.0.0 默认配置自动迁移到 1.1.0；管理员自定义过的额度不会被覆盖。
- 新增分阶段新手教程与 `/land tutorial`。
- 新手教程阶段写入 `data.yml`，支持跨重启继续。
- 创建确认 GUI、领地列表、管理中心、扩建、额度商店等统一改为“平面范围/平面额度”表述。

## 自动测试

执行：

```text
./test.sh
```

覆盖：

- 领地 XZ 几何、面积、包含、重叠、最小间距与 Chunk 覆盖
- 明确验证领地保护高度为 Y=0~255
- Owner/ADMIN/MEMBER/VISITOR/PUBLIC 权限
- 黑名单与保护决策
- 领地容量、额度与单块上限
- 领地序列化
- 两点选择状态
- 边界采样
- 额度购买计算
- GUI Context 路由
- 保存版本竞争保护
- 管理员搜索
- 新手教程启动、单向推进、完成、重启与状态快照恢复

期望：13 个测试全部 PASS。

## 构建验证

执行：

```text
./build.sh
```

结果目标：生成 `dist/YXLand-1.1.0.jar`。

额外检查：

- Java 主类字节码 major version 52（Java 8）
- JAR 不包含 `org/bukkit/` 离线编译桩
- `plugin.yml` / `config.yml` / `messages.yml` 可被 YAML 解析
- `pom.xml` 可被 XML 解析
- 源码无 TODO/FIXME/TBD 占位实现

## 运行时限制

当前环境没有完整可启动的 Spigot/Paper/CatServer 1.12.2 实例，因此本报告不宣称完成真实多人服务器运行测试。真实混合端中，模组机器保护能力仍取决于对应核心是否向 Bukkit 侧派发相关交互事件。
