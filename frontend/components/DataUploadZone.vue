<template>
  <section class="space-y-2">
    <UCard
      ref="dropZoneRef"
      class="text-sm flex justify-center items-center h-40"
      :class="{ '!border-blue-300 !bg-blue-100': isOverDropZone }"
      @click="open()"
    >
      <span>Drag and drop RSSI sample files or </span>

      <UButton
        class="inline-block text-xs ml-1"
        color="white"
        size="sm"
        variant="solid"
        @click.stop="open()"
      >
        select files
      </UButton>
    </UCard>

    <DataUploadZoneFile
      v-for="file in files"
      :key="file.name"
      :file="file"
      @remove="removeFile(file.name)"
    />
  </section>
</template>

<script setup lang="ts">
import { useDropZone, useFileDialog } from '@vueuse/core'

const files = defineModel<File[]>({ required: true })

// adds file to list of files
function addFile(file: File) {
  if (!files.value.find(f => f.name === file.name)) {
    files.value.push(file)
  }
  // TODO: surface to user that file exists
}

// adds files in file list
function addFileList(fileList: FileList) {
  for (let idx = 0; idx < fileList.length; idx++) {
    const file = fileList.item(idx) as File
    addFile(file)
  }
}

// removes file given filename
function removeFile(filename: string) {
  const file = files.value.find(f => filename === f.name)
  if (file) {
    const idx = files.value.indexOf(file)
    files.value.splice(idx, 1)
  }
}

const { files: dialogFiles, open } = useFileDialog({
  accept: 'text/csv',
})

watch(dialogFiles, () => dialogFiles.value ? addFileList(dialogFiles.value) : null)

const dropZoneRef = ref<HTMLDivElement>()
const { isOverDropZone } = useDropZone(dropZoneRef, {
  dataTypes: ['text/csv'],
  onDrop: (droppedFiles, _) => droppedFiles?.forEach(f => addFile(f)),
})
</script>
