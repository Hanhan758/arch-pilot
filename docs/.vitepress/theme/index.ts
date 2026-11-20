import DefaultTheme from 'vitepress/theme'
import type { Theme } from 'vitepress'
import PromptCopyCard from './components/PromptCopyCard.vue'
import GlossaryBadge from './components/GlossaryBadge.vue'
import ChecklistInteractive from './components/ChecklistInteractive.vue'
import './custom.css'

export default {
  extends: DefaultTheme,
  enhanceApp({ app }) {
    app.component('PromptCopyCard', PromptCopyCard)
    app.component('GlossaryBadge', GlossaryBadge)
    app.component('ChecklistInteractive', ChecklistInteractive)
  }
} satisfies Theme
