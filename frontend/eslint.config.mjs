// @ts-check
import antfu from '@antfu/eslint-config'
import withNuxt from './.nuxt/eslint.config.mjs'

export default await withNuxt(
  antfu(),
).override('antfu/vue/rules', {
  rules: {
    'vue/block-order': ['error', {
      order: ['template', 'script', 'style'],
    }],
  },
})
