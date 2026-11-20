# 主流 AI 平台安装与接入指南

无论你用的是网页版聊天 AI，还是桌面端的智能体编程工具，都可以按下面对应方式把 ArchPilot 3 合 1 套件接进去。

---

## 一、网页端与通用聊天 AI（零配置，10 秒上手）

适用：**ChatGPT、Claude.ai、DeepSeek、Kimi、豆包、通义千问** 等所有对话窗口。

### 方式 A：单次对话即插即用
1. 点开本站左侧栏对应的助手页（如 [苏格拉底零基础导师](/ai-kit/tutor)）；
2. 点击页面上的 **“一键复制提示词”** 按钮；
3. 新建一个 AI 对话，把提示词作为**第一条消息**直接发送，AI 就会立刻进入对应的角色并引导你开始。

### 方式 B：存成长期专属项目 / 自定义指令（推荐）
- **ChatGPT**：点左下角头像 → **Projects（项目）** → 新建一个 `架构学习与验货` 项目 → 把 `arch-tutor` 或 `arch-examiner` 内容放进 **Project Instructions（项目指令）**。
- **Claude**：进入 **Projects** → 新建项目 → 粘贴进 **Project Instructions**，以后这个项目里开的所有新对话都会自动保持“零黑话大白话模式”。

---

## 二、本地编程智能体（安装标准 `SKILL.md`）

适用：**Antigravity、Claude Code、Cursor、Codex** 等能读取本地文件夹的 AI 工具。安装后，不仅能在对话里随时呼出导师和考官，还能让 **`arch-auditor`** 自动帮你做只读项目体检。

### 1. 复制套件文件夹到你的本地 Skills 目录
在你的终端中（假定已把 `arch-pilot` 放在本地目录），根据你使用的客户端把 `skills/arch-*` 文件夹放到对应的全局技能目录即可：

| 客户端 / 平台 | 常见 Skill 存放位置与激活方式 |
| :--- | :--- |
| **Antigravity** | 将 `skills/arch-tutor`、`skills/arch-examiner`、`skills/arch-auditor` 放入你的全局或工作区 `skills/` 目录，对话中直接说“启用 arch-auditor 帮我体检当前项目”即可。 |
| **Claude Code** | 复制到用户目录 `~/.claude/skills/`（或项目级 `.claude/skills/`）下对应的子目录（保留其中的 `SKILL.md`），重启会话后即可用 `/arch-tutor` 或自然语言呼出。 |
| **Cursor** | 可将 `skills/arch-auditor/SKILL.md` 的内容添加到项目 `.cursor/rules/` 规则中（或支持 `SKILL.md` 的插件目录），让 AI 在动手改代码前自动受这套规则约束。 |
| **Codex / 通用 `AGENTS.md` 兼容工具** | 复制到对应的 `~/.codex/skills/` 目录，或在会话里直接指定读取 `skills/arch-auditor/SKILL.md`。 |

---

## 三、接入后的安全自查小提示

- 当你启用 `arch-auditor` 体检自己的真实项目时，如果工具询问“是否允许运行写命令或改文件”，**请果断拒绝写权限**——合格的体检只用只读能力就够了，真正的修改应当等看完《大白话架构体检报告》、由你拍板后再单独发起。
