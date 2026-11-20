<script setup>
import auditorPrompt from '../../prompts/arch-auditor.prompt.md?raw'
</script>

# 3. 真实项目体检助手（`arch-auditor`）

## 什么时候需要它？

当你自己用 AI（Cursor / Claude Code / ChatGPT 等）折腾出一个能跑的小项目，却开始隐隐感觉“越加功能越容易把老功能改崩”、“不知道哪些文件缠在了一起”、“怕不小心把隐私路径写进了公开区”——让它帮你做一次 **100% 只读、绝不改代码的《大白话架构体检报告》**。

---

## 一键获取通用提示词（网页对话版）

<PromptCopyCard
  title="真实项目大白话架构体检助手（arch-auditor v0.1.0）"
  badge="通用 Prompt · 只读诊断 · v0.1.0"
  description="在网页版 AI 中使用：先发送这段提示词，再把你的项目目录树和简短功能描述发给它。"
  :content="auditorPrompt"
  :default-expanded="false"
/>

---

## 你能拿到什么样的体检单？

体检助手不会扔给你满屏专业报错，而是固定输出 4 块内容：
1. **红 / 黄 / 绿灯总览**：分别给“模块边界”“数据与隐私安全”“自动验货防线”“可移植性”打灯说明；
2. **最危险的前 3 个隐患**：用生活类比讲清楚如果不修、继续往里堆功能会炸在哪里；
3. **不推倒重写的 3 步最小改进顺序**：教你先补哪道护栏、再拆哪两个文件；
4. **可直接复制发给编程 AI 的修复指令**：自带“先列清单、不动无关文件、跑完测试再交差”的约束。

> **本地自动扫描建议**：如果你在用具备读文件能力的编程 Agent（如 Antigravity、Claude Code、Cursor），推荐直接安装本仓库的 **`skills/arch-auditor/SKILL.md`**，它会自动以严格只读方式盘点目录树并做隐私脱敏，无需手动复制粘贴文件列表。
