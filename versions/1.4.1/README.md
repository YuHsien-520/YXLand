# YXLand 1.4.1

Minecraft Java Edition 1.12.2 永久领地保护与 AdminRegion 系统领域插件。

## 1.4.1 重点

- 进入/离开 Title、Subtitle、ActionBar、Chat 可独立开关。
- Subtitle 不再依附 Title；只开启 Subtitle 也可以正确显示。
- 编辑展示文本后立即预览，并提供“预览进入效果 / 预览离开效果”。
- AdminRegion 规则扩展为 37 条，按 6 类管理：建造与物品、战斗与伤害、移动与传送、生物与生成、世界环境、系统与自动化。
- 所有规则继续使用 INHERIT / ALLOW / DENY 三态与优先级解析。
- 新增/补强丢弃、拾取、物品使用、非PVP伤害、弹射物、药水、传送、末影珍珠、传送门、载具、生物生成、结构生长、树叶腐烂、冰雪、自然方块形成、命令等事件保护。
- 1.4.0 旧领域新增规则默认 INHERIT，旧 Subtitle 开关按原 Title 开关兼容迁移。
- config-version: 9。

## 源码归档

`source-archive/` 内保存完整 1.4.1 源码树的无损十六进制分片。按文件名顺序拼接后执行 `bytes.fromhex()` 即可还原 `YXLand-1.4.1-source-tree.tar.xz`。

源码归档 SHA256：`3e37ce14840369ffc3ecd0b61bb740048e732de41af7aad6c2a408d37fd8b8b5`
