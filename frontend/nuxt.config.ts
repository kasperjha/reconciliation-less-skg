// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  devtools: { enabled: true },
  modules: ['@nuxtjs/tailwindcss', '@nuxt/eslint'],
  compatibilityDate: '2024-07-18',
  eslint: {
    config: {
      standalone: false,
    },
  },
})
