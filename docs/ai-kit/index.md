# 3 合 1 AI 陪学与验货套件

为了让你既能在网页端聊天窗口里随时学，又能让本地编程 AI 自动遵守工程规矩，ArchPilot 把全部能力统一做成了 **两种等价格式**（当前全量升级至 **`v1.0.0`**）：

1. **通用 Prompt 版**：点击下方各工具页的 **“一键复制提示词”**，直接粘贴进 ChatGPT、Claude、DeepSeek、Kimi 或豆包即可使用，零安装门槛。
2. **标准 Agent Skill 版**：仓库根目录 `skills/` 文件夹中已按标准 `SKILL.md` 规范打包好，可直接安装进 Antigravity、Claude Code、Cursor 或 Codex。

---

## 三大核心助手怎么选？

| 工具 | 它干什么用？ | 什么时候找它？ | 前往获取 |
| :--- | :--- | :--- | :--- |
| **1. 苏格拉底零基础导师**<br>`arch-tutor` | 禁止堆砌黑话，用生活类比 + 极简图解逐层带你学，每次只问 1 个理解确认题 | 读每周教程卡壳、或遇到 AI 扔过来一堆陌生名词看不懂时 | [去使用导师 →](/ai-kit/tutor) |
| **2. “老板验货”模拟考官**<br>`arch-examiner` | 先装成“爱走捷径的程序员 AI”交一份带 2–3 个隐蔽暗坑的方案，等你挑刺盘问完再按 100 分制复盘打分 | 每周学完一章做实战巩固，练就“老板审方案”的条件反射 | [去挑战考官 →](/ai-kit/examiner) |
| **3. 真实项目体检助手**<br>`arch-auditor` | **严格只读、不改任何文件**，扫描你的真实 AI 编程项目，输出红/黄/绿灯大白话体检报告和最小修复指令 | 你自己手里已经用 AI 写了一个项目，感觉越改越乱想查病因时 | [去给项目体检 →](/ai-kit/auditor) |

---

## 配套实战资源

- **没打开 AI 也能先自测**：[“老板验货”经典 6 关题库自测（离线版）](/ai-kit/exam-bank)
- **不知道怎么装进自己的软件？**：[主流 AI 平台安装与接入指南](/ai-kit/install-guides)

---

## 在本地 Agent 里安装 Skill 版（速览）

如果你日常使用支持 Agent Skill 的工具（如 Antigravity / Claude Code / Cursor），只需要把仓库中的 `skills/` 下对应目录复制到你的 Agent Skills 目录即可自动识别：

```text
skills/
├── arch-tutor/SKILL.md
├── arch-examiner/SKILL.md
└── arch-auditor/SKILL.md
```
