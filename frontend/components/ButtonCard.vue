<template>
  <NuxtLink
    :to="to"
    class="block"
    :disabled="disabled"
  >
    <button :disabled="disabled" class="w-full h-full hover:bg-gray-200 rounded p-10 border border-gray-400 bg-gray-100 flex justify-center items-center disabled:hover:bg-gray-50 disabled:opacity-50">
      <slot />
    </button>
  </NuxtLink>
</template>

<script lang="ts" setup>
interface Props {
  to?: string
  disabled?: boolean
}
defineProps<Props>()
</script>
