<template>
  <ContainerRounded>
    <UTable
      v-model="selectedDisplayFiles"
      :columns
      :rows="displayFiles"
    />
  </ContainerRounded>

  <div class="flex flex-wrap gap-1">
    <UButton
      color="white"
      :disabled="!selectedDisplayFiles.length"
      icon="i-heroicons-trash-20-solid"
      @click="removeSelectedFiles"
    >
      Remove file(s)
    </UButton>
  </div>
</template>

<script lang="ts" setup>
const files = defineModel<File[]>({ required: true })
const columns = [
  { key: 'name', label: 'Filename' },
  { key: 'DeviceId', label: 'Device ID' },
]

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
  selectedDisplayFiles.value.forEach(f => removeFile(f.id))
  selectedDisplayFiles.value = []
}
</script>
