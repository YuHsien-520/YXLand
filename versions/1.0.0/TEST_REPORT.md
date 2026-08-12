# YXLand 1.0.0 交付验证报告

验证日期：2026-08-09
目标：Minecraft Java Edition 1.12.2 / Java 8

## 自动测试

执行：`./test.sh`

结果：12/12 核心回归测试通过。

覆盖：
- 领地几何、面积、包含、重叠、最小间距与 Chunk 覆盖
- 成员角色、公开权限、黑名单与环境 Flag
- Chunk 空间索引、创建/扩建/转让容量校验
- 基础/购买额度与溢出保护
- 数据快照序列化往返
- 两点选择与扩建选择状态
- 方块/液体/活塞等保护决策
- 玩家专属边界采样
- Vault 额度购买数值校验
- GUI 路由上下文
- 异步保存版本竞争与关服屏障
- 管理员领地搜索

## 构建验证

执行：`./build.sh`

结果：生成 `dist/YXLand-1.0.0.jar`。

检查：
- 主类 class major version = 52（Java 8）
- JAR 含 `plugin.yml`、`config.yml`、`messages.yml`
- JAR 不包含 `org/bukkit/**` 离线编译桩
- `plugin.yml` / `config.yml` / `messages.yml` 均通过 YAML 解析
- `pom.xml` 通过 XML 解析
- `build.sh` / `test.sh` 通过 shell 语法检查
- 生产源码与测试中没有 TODO/FIXME/TBD 占位标记

## 保护与稳定性审查

- 保护查找使用 world + chunk 空间索引，事件热路径不全量扫描所有领地。
- 单领地设置 16,384 Chunk 技术索引上限，防止异常超大坐标拖垮索引。
- GUI 使用专用 InventoryHolder，并拦截顶部 GUI 点击与拖拽。
- 多方块放置逐 BlockState 校验，防止门/床等跨边界绕过。
- 液体跨野外/领地、领地/领地边界被拦截；领地内部受 FLUID Flag 控制。
- 领地边界由一个统一任务维护，且仅发送给请求查看的玩家。
- 持久化采用快照 + Dirty + 异步写入；版本校验、单写锁和关服屏障避免旧异步快照覆盖新数据。
- 数据加载失败时不允许关服流程用空状态覆盖原数据文件。

## 当前环境限制

当前容器没有 Maven，也没有可直接运行的真实 Spigot/Paper/CatServer 1.12.2 服务端 JAR，因此本次不能完成“启动一台真实 1.12.2 服务器并进服点击 GUI”的运行时烟雾测试。

为避免把环境限制伪装成真实服务器验证，本项目提供：
- `pom.xml`：生产环境使用实际 `spigot-api:1.12.2-R0.1-SNAPSHOT` 编译。
- `compile-stubs/`：仅用于当前离线环境的 Java 8/API 结构静态编译，构建脚本会强制检查这些桩没有进入插件 JAR。

模组机器的最终拦截范围取决于所用 CatServer/混合端是否把该模组交互转发为 Bukkit 事件。特殊纯 Forge 交互如果绕过 Bukkit，需要针对具体模组增加 Hook。
