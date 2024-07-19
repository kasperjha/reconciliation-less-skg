<template>
  <main>
    <h1>Manually ingest samples</h1>
    <p>
      Here files can be ingested into the system by hand.
    </p>

    <h2>Select collection</h2>
    <p>
      All uploaded samples belong to a collection.
      Select which collection these sample should belong to.
    </p>

    <CollectionPicker v-model="selectedCollectionId" class="mt-4" />
    <UButton
      class="mt-2"
      color="white"
      icon="i-heroicons-arrow-top-right-on-square-20-solid"
      trailing
      @click="onNewCollection"
    >
      New collection
    </UButton>

    <h2>Select files</h2>

    <p>
      <!-- TODO: research and document file structure -->
      The RSSI data files require a specific data structure.
      They must be in `csv` format and have one column with integer valued cells.
    </p>

    <SampleDropZone v-model="files" />

    <h2>Manage files</h2>
    <p>
      Sepecify metadata about the collected RSSI measurements.
    </p>

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
  selectedDisplayFiles.value.forEach(f => removeFile(f.id))
  selectedDisplayFiles.value = []
}

const selectedCollectionId = ref(null)
function onNewCollection() {
  navigateTo('/collections')
}
</script>
