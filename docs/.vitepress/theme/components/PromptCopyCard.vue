<script setup lang="ts">
import { computed, ref } from 'vue'

const props = withDefaults(
  defineProps<{
    title: string
    badge?: string
    description?: string
    content: string
    defaultExpanded?: boolean
  }>(),
  {
    badge: '通用 Prompt',
    description: '',
    defaultExpanded: false
  }
)

const expanded = ref(props.defaultExpanded)
const copied = ref(false)

const cleanContent = computed(() => {
  const raw = (props.content || '').trim()
  if (raw.startsWith('---')) {
    const end = raw.indexOf('\n---', 3)
    if (end !== -1) {
      return raw.slice(end + 4).trim()
    }
  }
  return raw
})

async function copyPrompt() {
  if (typeof window === 'undefined') return
  const text = cleanContent.value
  try {
    if (navigator?.clipboard?.writeText) {
      await navigator.clipboard.writeText(text)
    } else {
      const textarea = document.createElement('textarea')
      textarea.value = text
      textarea.setAttribute('readonly', '')
      textarea.style.position = 'fixed'
      textarea.style.opacity = '0'
      document.body.appendChild(textarea)
      textarea.select()
      document.execCommand('copy')
      document.body.removeChild(textarea)
    }
    copied.value = true
    window.setTimeout(() => {
      copied.value = false
    }, 2200)
  } catch {
    expanded.value = true
  }
}
</script>

<template>
  <div class="ap-card">
    <div class="ap-prompt-header">
      <div>
        <div class="ap-prompt-title-row">
          <span class="ap-prompt-badge">{{ badge }}</span>
          <strong class="ap-prompt-title">{{ title }}</strong>
        </div>
        <p v-if="description" class="ap-prompt-desc">{{ description }}</p>
      </div>
      <div class="ap-prompt-actions">
        <button type="button" class="ap-btn" @click="copyPrompt">
          {{ copied ? '已复制提示词' : '一键复制提示词' }}
        </button>
        <button
          type="button"
          class="ap-btn ap-btn-secondary"
          @click="expanded = !expanded"
        >
          {{ expanded ? '收起正文' : '展开查看' }}
        </button>
      </div>
    </div>

    <pre v-if="expanded" class="ap-prompt-pre"><code>{{ cleanContent }}</code></pre>
  </div>
</template>

<style scoped>
.ap-prompt-header {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  align-items: flex-start;
  gap: 12px;
}

.ap-prompt-title-row {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.ap-prompt-badge {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 600;
  background: var(--vp-c-brand-soft);
  color: var(--vp-c-brand-1);
}

.ap-prompt-title {
  font-size: 16px;
}

.ap-prompt-desc {
  margin: 6px 0 0;
  font-size: 14px;
  color: var(--vp-c-text-2);
}

.ap-prompt-actions {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.ap-prompt-pre {
  margin: 14px 0 0;
  padding: 14px;
  border-radius: 8px;
  background: var(--vp-c-bg-alt);
  border: 1px solid var(--vp-c-divider);
  max-height: 420px;
  overflow: auto;
  font-size: 13px;
  line-height: 1.6;
  white-space: pre-wrap;
  word-break: break-word;
}
</style>
