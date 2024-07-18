<template>
  <div
    ref="dropZoneRef"
    class="flex text-sm h-40  text-gray-600 items-center gap-2 justify-center rounded border-gray-200 border bg-gray-50 p-10"
    :class="{ '!border-blue-300 !bg-blue-100': isOverDropZone }"
  >
    <p>
      Drop your CSV files with RSSI samples here
      <Icon
        name="heroicons:document-chart-bar-20-solid"
        class="size-5"
      />
    </p>
  </div>
</template>

<script setup lang="ts">
import { useDropZone } from '@vueuse/core'

const dropZoneRef = ref<HTMLDivElement>()
const { isOverDropZone } = useDropZone(dropZoneRef, {
  dataTypes: ['text/csv'],
})
</script>
