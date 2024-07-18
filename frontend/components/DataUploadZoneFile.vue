<template>
  <UCard>
    <div class="w-full flex items-center">
      <Icon name="heroicons:document-chart-bar-20-solid" class="size-5 mr-2" />
      <span class="truncate text-ellipsis">{{ file.name }}</span>
      <UButton
        size="lg"
        icon="i-heroicons-x-mark"
        color="white"
        class="ml-auto"
        @click="$emit('remove')"
      />
    </div>
  </UCard>
</template>

<script lang="ts" setup>
interface Props {
  file: File
}
defineProps<Props>()
defineEmits(['remove'])
</script>
