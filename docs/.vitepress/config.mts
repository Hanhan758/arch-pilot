import { defineConfig } from 'vitepress'
import { withMermaid } from 'vitepress-plugin-mermaid'

export default withMermaid(
  defineConfig({
    lang: 'zh-CN',
    title: 'ArchPilot',
    description: 'AI 时代零基础架构思维与工程总控开源指南',
    cleanUrls: true,
    lastUpdated: false,
    themeConfig: {
      siteTitle: 'ArchPilot',
      nav: [
        { text: '起步指南', link: '/guide/start' },
        { text: '6 周学习地图', link: '/guide/week-01-data-rules' },
        { text: 'TALOS-Lite 案例', link: '/talos-lite/overview' },
        { text: '常备工具箱', link: '/toolkit/glossary' },
        { text: 'AI 陪学套件', link: '/ai-kit/' }
      ],
      sidebar: {
        '/guide/': [
          {
            text: '起步与地图',
            items: [
              { text: '零基础总控避坑指南', link: '/guide/start' }
            ]
          },
          {
            text: '6 周实战学习路线',
            items: [
              { text: 'Week 1：数据与规则地基', link: '/guide/week-01-data-rules' },
              { text: 'Week 2：版本控制与真假账本（预习）', link: '/guide/week-02-git-truth' },
              { text: 'Week 3：架构思维与单向分层（预习）', link: '/guide/week-03-oop-layers' },
              { text: 'Week 4：并发、事务与人机隔离（预习）', link: '/guide/week-04-concurrency-guard' },
              { text: 'Week 5：自动化测试与无损重构（预习）', link: '/guide/week-05-tdd-migration' },
              { text: 'Week 6：平台边界与打包分发（预习）', link: '/guide/week-06-packaging-boundary' }
            ]
          }
        ],
        '/talos-lite/': [
          {
            text: '脱敏教学标杆模型',
            items: [
              { text: 'TALOS-Lite 6 大积木全景', link: '/talos-lite/overview' }
            ]
          }
        ],
        '/toolkit/': [
          {
            text: '总控常备工具箱',
            items: [
              { text: '大白话术语翻译表', link: '/toolkit/glossary' },
              { text: '总控审校 AI 10 条反问清单', link: '/toolkit/review-checklist' }
            ]
          }
        ],
        '/ai-kit/': [
          {
            text: '3 合 1 AI 陪学套件',
            items: [
              { text: '套件总览与安装说明', link: '/ai-kit/' },
              { text: '1. 苏格拉底零基础导师', link: '/ai-kit/tutor' },
              { text: '2. “老板验货”模拟考官', link: '/ai-kit/examiner' },
              { text: '3. 真实项目体检助手', link: '/ai-kit/auditor' }
            ]
          }
        ]
      },
      search: {
        provider: 'local',
        options: {
          translations: {
            button: {
              buttonText: '搜索概念或清单',
              buttonAriaLabel: '搜索概念或清单'
            },
            modal: {
              noResultsText: '没有找到相关内容，试试换个大白话关键词',
              resetButtonTitle: '清空搜索',
              footer: {
                selectText: '选择',
                navigateText: '切换',
                closeText: '关闭'
              }
            }
          }
        }
      },
      outline: {
        level: [2, 3],
        label: '本页目录'
      },
      docFooter: {
        prev: '上一节',
        next: '下一节'
      },
      returnToTopLabel: '回到顶部',
      sidebarMenuLabel: '菜单',
      darkModeSwitchLabel: '外观主题'
    },
    mermaid: {},
    vite: {
      optimizeDeps: {
        include: ['mermaid']
      }
    }
  })
)
