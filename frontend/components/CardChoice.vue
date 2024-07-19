<template>
  <NuxtLink
    :to="disabled ? '' : to"
    class="hover:brightness-90"
    :class="{ 'opacity-50 !brightness-100': disabled }"
  >
    <UCard class="h-full ">
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
