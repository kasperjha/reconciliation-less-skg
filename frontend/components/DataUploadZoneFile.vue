<template>
  <article class="p-4 flex gap-6 items-center border bg-gray-50 rounded">
    <Icon name="heroicons:document-chart-bar-20-solid" class="size-5" />
    <span class="truncate text-ellipsis">{{ file.name }}</span>
    <button
      class="ml-auto flex justify-center items-center p-1 rounded hover:bg-gray-200"
      @click="$emit('remove')"
    >
      <Icon name="heroicons:x-mark-20-solid" class="size-5" />
    </button>
  </article>
</template>

<script lang="ts" setup>
interface Props {
  file: File
}
defineProps<Props>()
defineEmits(['remove'])
</script>
