<template>
  <NuxtLink :to="to" class="block">
    <button class="w-full h-full hover:bg-gray-100 rounded p-10 border border-gray-400 bg-gray-50 flex justify-center items-center">
      <slot />
    </button>
  </NuxtLink>
</template>

<script lang="ts" setup>
interface Props {
  to?: string
}
defineProps<Props>()
</script>
