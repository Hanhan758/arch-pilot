<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'

export interface ChecklistItem {
  id: string
  stage: string
  title: string
  prompt: string
  dangerSignal?: string
}

const props = withDefaults(
  defineProps<{
    items: ChecklistItem[]
    storageKey?: string
  }>(),
  {
    storageKey: 'arch-pilot-review-checklist-v1'
  }
)

const checkedIds = ref<string[]>([])
const copiedNotice = ref('')

onMounted(() => {
  try {
    const saved = window.localStorage.getItem(props.storageKey)
    if (saved) {
      const parsed = JSON.parse(saved)
      if (Array.isArray(parsed)) {
        checkedIds.value = parsed.filter((id): id is string => typeof id === 'string')
      }
    }
  } catch {
    checkedIds.value = []
  }
})

function persist() {
  if (typeof window === 'undefined') return
  try {
    window.localStorage.setItem(props.storageKey, JSON.stringify(checkedIds.value))
  } catch {
    // ignore storage quota errors
  }
}

function toggleItem(id: string) {
  if (checkedIds.value.includes(id)) {
    checkedIds.value = checkedIds.value.filter((item) => item !== id)
  } else {
    checkedIds.value = [...checkedIds.value, id]
  }
  persist()
}

function resetAll() {
  checkedIds.value = []
  persist()
}

const totalCount = computed(() => props.items.length)
const doneCount = computed(() =>
  props.items.filter((item) => checkedIds.value.includes(item.id)).length
)
const progressPercent = computed(() =>
  totalCount.value === 0 ? 0 : Math.round((doneCount.value / totalCount.value) * 100)
)

const groupedItems = computed(() => {
  const groups: Array<{ stage: string; items: ChecklistItem[] }> = []
  for (const item of props.items) {
    const existing = groups.find((group) => group.stage === item.stage)
    if (existing) {
      existing.items.push(item)
    } else {
      groups.push({ stage: item.stage, items: [item] })
    }
  }
  return groups
})

async function copyQuestions(onlyUnchecked: boolean) {
  if (typeof window === 'undefined') return
  const target = onlyUnchecked
    ? props.items.filter((item) => !checkedIds.value.includes(item.id))
    : props.items
  if (target.length === 0) {
    copiedNotice.value = '所有条目已全部核验通过'
    window.setTimeout(() => {
      copiedNotice.value = ''
    }, 2000)
    return
  }
  const text =
    '请逐条对照以下工程审校问题，基于真实文件和实际运行结果如实回答：\n\n' +
    target.map((item, idx) => `${idx + 1}. [${item.title}] ${item.prompt}`).join('\n')
  try {
    await navigator.clipboard.writeText(text)
    copiedNotice.value = onlyUnchecked
      ? `已复制未核验的 ${target.length} 条反问`
      : `已复制全部 ${target.length} 条反问`
    window.setTimeout(() => {
      copiedNotice.value = ''
    }, 2200)
  } catch {
    copiedNotice.value = '浏览器拦截了剪贴板，请手动复制下方清单'
  }
}
</script>

<template>
  <div class="ap-card">
    <div class="ap-cl-top">
      <div>
        <div class="ap-cl-stats">
          <strong>当前已核验 {{ doneCount }} / {{ totalCount }} 项</strong>
          <span class="ap-cl-pct">（{{ progressPercent }}%）</span>
        </div>
        <div class="ap-cl-bar-bg">
          <div class="ap-cl-bar-fill" :style="{ width: `${progressPercent}%` }" />
        </div>
      </div>

      <div class="ap-cl-actions">
        <button type="button" class="ap-btn" @click="copyQuestions(true)">
          复制未核验条目发给 AI
        </button>
        <button type="button" class="ap-btn ap-btn-secondary" @click="copyQuestions(false)">
          复制全部 10 条
        </button>
        <button type="button" class="ap-btn ap-btn-secondary" @click="resetAll">
          重置勾选
        </button>
      </div>
    </div>

    <p v-if="copiedNotice" class="ap-cl-notice">{{ copiedNotice }}</p>

    <div v-for="group in groupedItems" :key="group.stage" class="ap-cl-group">
      <h3 class="ap-cl-stage">{{ group.stage }}</h3>
      <label
        v-for="item in group.items"
        :key="item.id"
        class="ap-cl-item"
        :class="{ checked: checkedIds.includes(item.id) }"
      >
        <input
          type="checkbox"
          :checked="checkedIds.includes(item.id)"
          @change="toggleItem(item.id)"
        />
        <div class="ap-cl-body">
          <div class="ap-cl-title">
            <span class="ap-cl-id">{{ item.id }}</span>
            <span>{{ item.title }}</span>
          </div>
          <div class="ap-cl-prompt">“{{ item.prompt }}”</div>
          <div v-if="item.dangerSignal" class="ap-cl-danger">
            危险信号：{{ item.dangerSignal }}
          </div>
        </div>
      </label>
    </div>
  </div>
</template>

<style scoped>
.ap-cl-top {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  align-items: center;
  gap: 14px;
  padding-bottom: 14px;
  border-bottom: 1px solid var(--vp-c-divider);
}

.ap-cl-stats {
  font-size: 15px;
}

.ap-cl-pct {
  color: var(--vp-c-text-2);
  font-size: 13px;
}

.ap-cl-bar-bg {
  margin-top: 8px;
  width: 240px;
  max-width: 100%;
  height: 8px;
  border-radius: 999px;
  background: var(--vp-c-bg-alt);
  overflow: hidden;
  border: 1px solid var(--vp-c-divider);
}

.ap-cl-bar-fill {
  height: 100%;
  background: var(--vp-c-brand-1);
  transition: width 0.2s ease;
}

.ap-cl-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.ap-cl-notice {
  margin: 10px 0 0;
  font-size: 13px;
  font-weight: 600;
  color: var(--vp-c-brand-1);
}

.ap-cl-group {
  margin-top: 18px;
}

.ap-cl-stage {
  margin: 0 0 10px;
  font-size: 15px;
  color: var(--vp-c-brand-1);
}

.ap-cl-item {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  padding: 10px 12px;
  border-radius: 8px;
  border: 1px solid var(--vp-c-divider);
  background: var(--vp-c-bg);
  margin-bottom: 8px;
  cursor: pointer;
}

.ap-cl-item.checked {
  opacity: 0.72;
  background: var(--vp-c-bg-alt);
}

.ap-cl-item input {
  margin-top: 4px;
  width: 16px;
  height: 16px;
  accent-color: var(--vp-c-brand-1);
}

.ap-cl-body {
  flex: 1;
}

.ap-cl-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
  font-size: 14px;
}

.ap-cl-id {
  font-family: var(--vp-font-family-mono);
  font-size: 12px;
  padding: 1px 6px;
  border-radius: 4px;
  background: var(--vp-c-brand-soft);
  color: var(--vp-c-brand-1);
}

.ap-cl-prompt {
  margin-top: 4px;
  font-size: 14px;
  color: var(--vp-c-text-1);
}

.ap-cl-danger {
  margin-top: 4px;
  font-size: 12px;
  color: var(--vp-c-text-2);
}
</style>
