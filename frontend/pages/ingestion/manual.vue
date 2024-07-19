<template>
  <main>
    <h1>Manually ingest samples</h1>
    <DataUploadZone v-model="files" />
  </main>
</template>

<script lang="ts" setup>
const files = ref<File[]>([])
</script>
