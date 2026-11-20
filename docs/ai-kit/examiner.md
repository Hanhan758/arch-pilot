<script setup>
import examinerPrompt from '../../prompts/arch-examiner.prompt.md?raw'
</script>

# 2. “老板验货”模拟考官（`arch-examiner`）

## 为什么要专门练“挑刺”？

只看懂概念，不代表当编程 AI 满口保证“方案很完善”时你能反应过来它偷了懒。`arch-examiner v1.0.0` 会先假扮成一位**客客气气、但偷偷图省事的研发 AI**，向你汇报一份藏有 **2–3 个真实工程暗坑** 的方案——由你扮演老板拿着 [10 条反问清单](/toolkit/review-checklist) 去盘问它，最后再切换考官按 **100 分制 4 维权重**（防越权与隐私 30 分 / 数据一致性与并发 25 分 / 模块分层与解耦 25 分 / 测试与稳健演进 20 分）给你复盘打分。

---

## 一键获取通用提示词（ChatGPT / Claude / DeepSeek 通用）

<PromptCopyCard
  title="“老板验货”模拟考官（arch-examiner v1.0.0）"
  badge="通用 Prompt · v1.0.0"
  description="复制后发给任意 AI，选定 Week 1–6 或“综合大考”，开始一轮 5 分钟的审校对抗练习。"
  :content="examinerPrompt"
  :default-expanded="false"
/>

---

## 推荐练法（3 步走）

1. **选定关卡**：告诉考官“*请开启 Week 4 关卡*”（支持 Week 1–6 每周 2 套轮换题库，或直接选“*综合大考*”）。
2. **先别急着同意**：仔细看它交上来的“方案”，挑出最让你隐隐觉得不对劲的地方，用反问清单里的 2–3 句话去问它。
3. **查看评分与纠偏话术**：问完后回复“*我查完了，揭晓答案吧*”，考官会给你打出 0–100 分，并附上以后可直接复制去堵住真实编程 AI 的纠偏指令。

> **离线先刷一遍题？** 去 [“老板验货”经典 6 关题库自测（离线版）](/ai-kit/exam-bank) ｜ **Agent Skill 路径**：`skills/arch-examiner/SKILL.md`
