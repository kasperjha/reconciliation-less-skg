<template>
  <main>
    <h1>Manually ingest samples</h1>
    <SampleDropZone v-model="files" />

    <UTable v-model="selectedDisplayFiles" :rows="displayFiles" />

    <UButton
      color="red"
      class="mt-4"
      @click="removeSelectedFiles"
    >
      Remove File(s)
    </UButton>
  </main>
</template>

<script lang="ts" setup>
const files = ref<File[]>([])

function removeFile(fileIndex: number) {
  const temp = files.value
  temp.splice(fileIndex, 1)
  files.value = temp
}

interface DisplayFile {
  id: number
  name: string
}
const selectedDisplayFiles = ref<DisplayFile[]>([])
const displayFiles = computed<DisplayFile[]>(() => files.value.map(f => ({
  id: files.value.indexOf(f),
  name: f.name,
})))

function removeSelectedFiles() {
  console.log(selectedDisplayFiles.value)
  console.log('removing selected files:')
  console.log(selectedDisplayFiles.value)
  selectedDisplayFiles.value.forEach(f => removeFile(f.id))
  selectedDisplayFiles.value = []
}
</script>
