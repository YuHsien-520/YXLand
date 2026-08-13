# YXLand 1.4.1 更新日志

## 系统领域展示修复
- 进入/离开 Subtitle 改为独立开关，不再依赖 Title。
- 只启用 Subtitle 时仍会正确发送空 Title + Subtitle。
- 修改 Title / Subtitle / ActionBar / Chat 后立即预览。
- 增加进入/离开完整效果预览按钮。

## 系统领域规则中心
- AdminRegion 三态规则扩展为 37 条、6 个分类。
- 高优先级显式 ALLOW/DENY 优先；INHERIT 继续向低优先级领域解析。

## 事件保护补强
- 覆盖丢弃/拾取/使用物品、非PVP伤害、弹射物、药水、传送、末影珍珠、传送门、载具、生物生成、结构生长、树叶腐烂、冰雪、自然方块形成和命令。
- PLAYER_DAMAGE 排除玩家造成的伤害，避免和 PVP 重复拦截。

## 兼容
- Minecraft 1.12.2 / Java 8。
- config-version: 9。
- 旧 1.4.0 领域新增规则缺失时默认 INHERIT。
