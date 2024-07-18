<template>
  <div>
    <h1>Manually ingest samples</h1>
    <DataUploadZone v-model="files" />
  </div>
</template>

<script lang="ts" setup>
const files = ref<File[]>([])
</script>
