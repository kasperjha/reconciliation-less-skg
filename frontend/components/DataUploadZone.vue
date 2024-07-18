<template>
  <section class="space-y-2">
    <div
      ref="dropZoneRef"
      class="flex text-sm h-40 cursor-pointer items-center gap-1 justify-center rounded border-gray-600 border bg-gray-100 p-3"
      :class="{ '!border-blue-300 !bg-blue-100': isOverDropZone }"
      @click="open()"
    >
      <Icon name="heroicons:document-chart-bar" class="size-6" />
      <p>
        <span>Drop RSSI samples here, or</span>
        <button class="underline" @click.stop="open()">
          select files
        </button>
      </p>
    </div>
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
