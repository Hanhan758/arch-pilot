<script setup lang="ts">
import { computed } from 'vue'
import { withBase } from 'vitepress'

const props = withDefaults(
  defineProps<{
    category: string
    label?: string
    anchor?: string
  }>(),
  {
    label: '',
    anchor: ''
  }
)

const toneClass = computed(() => {
  if (props.category.includes('核心')) return 'tone-core'
  if (props.category.includes('分层') || props.category.includes('依赖')) return 'tone-layer'
  if (props.category.includes('安全') || props.category.includes('并发')) return 'tone-safety'
  return 'tone-quality'
})

const targetHref = computed(() => {
  if (!props.anchor) return ''
  const cleanAnchor = props.anchor.startsWith('#') ? props.anchor : `#${props.anchor}`
  return withBase(`/toolkit/glossary${cleanAnchor}`)
})
</script>

<template>
  <a v-if="targetHref" :href="targetHref" class="ap-glossary-badge" :class="toneClass">
    <span class="ap-dot" />
    <span>{{ label || category }}</span>
  </a>
  <span v-else class="ap-glossary-badge" :class="toneClass">
    <span class="ap-dot" />
    <span>{{ label || category }}</span>
  </span>
</template>

<style scoped>
.ap-glossary-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 2px 10px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 600;
  text-decoration: none;
  border: 1px solid transparent;
  vertical-align: middle;
}

.ap-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: currentColor;
}

.tone-core {
  color: #0f766e;
  background: rgba(15, 118, 110, 0.12);
}

.tone-layer {
  color: #1d4ed8;
  background: rgba(29, 78, 216, 0.12);
}

.tone-safety {
  color: #b45309;
  background: rgba(180, 83, 9, 0.14);
}

.tone-quality {
  color: #7c3aed;
  background: rgba(124, 58, 237, 0.12);
}

.dark .tone-core {
  color: #5eead4;
}

.dark .tone-layer {
  color: #93c5fd;
}

.dark .tone-safety {
  color: #fcd34d;
}

.dark .tone-quality {
  color: #c4b5fd;
}
</style>
