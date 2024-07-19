<template>
  <NuxtLink
    :to="to"
    :disabled="disabled"
  >
    <UCard class="hover:brightness-90 h-full">
      <p>
        {{ title }}
      </p>
      <p class="text-sm text-gray-600 mt-1">
        {{ description }}
      </p>
    </UCard>
  </NuxtLink>
</template>

<script lang="ts" setup>
interface Props {
  title: string
  description?: string
  to?: string
  disabled?: boolean
}
defineProps<Props>()
</script>
