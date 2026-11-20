## 本次改动说明
- 改动目的：
- 影响文件范围（如 `docs/guide/`、`prompts/`、`skills/` 等）：

## 合并前自检（对照 5 道自动化门禁）
- [ ] **GATE-01 隐私脱敏**：确认未出现任何本机绝对路径前缀、私人目录标识或真实凭据
- [ ] **GATE-02 示例精简**：若改动 `docs/talos-lite/examples/`，单文件严格 `<= 60` 行
- [ ] **GATE-03 套件同步**：若改动 `prompts/` 或 `skills/`，对应版本与站点页已同步更新
- [ ] **GATE-04 构建与死链**：`npm run docs:build` 已通过且无死链
- [ ] **GATE-05 可读性规范**：术语配有大白话类比，Mermaid 图无 HTML 标签
- [ ] **实测命令确认**：已在本地运行 `npm run check:all` 并全部绿灯通过
