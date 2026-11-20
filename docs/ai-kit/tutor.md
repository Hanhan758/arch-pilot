<script setup>
import tutorPrompt from '../../prompts/arch-tutor.prompt.md?raw'
</script>

# 1. 苏格拉底零基础架构导师（`arch-tutor`）

## 它能帮你解决什么问题？

普通 AI 回答技术问题时经常一口气甩出十几个英文缩写，越听越懵。`arch-tutor` 被设定为**强制遵守“先打生活比喻 → 再画极简关系图 → 每次只问 1 道确认题”**的私人导师，确保你真正听懂一个概念再往下走。

---

## 一键获取通用提示词（ChatGPT / Claude / DeepSeek 通用）

<PromptCopyCard
  title="苏格拉底零基础架构导师（arch-tutor v0.1.0）"
  badge="通用 Prompt · v0.1.0"
  description="复制后粘贴到任意 AI 对话窗口作为首条消息，即可开启按周带学或黑话实时翻译模式。"
  :content="tutorPrompt"
  :default-expanded="false"
/>

---

## 推荐开场对话示例

复制提示词发给 AI 后，它会自动问你想从哪开始。你可以直接这样回它：

- **跟学每周课程**：*“我刚看完 ArchPilot 的第 1 周，还是不太分得清 JSON 和 JSON Schema 在实战里到底各管什么，请用生活例子考考我。”*
- **现场翻译 AI 黑话**：*“刚才帮我写代码的 AI 说它要‘给这个模块加个适配器端口’，我不懂啥意思，帮我翻译成大白话。”*

> **Agent Skill 安装路径**：`skills/arch-tutor/SKILL.md`
