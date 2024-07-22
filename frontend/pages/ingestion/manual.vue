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

    <div class="flex gap-1">
      <CollectionPicker v-model="selectedCollectionId" class="flex-grow" />
      <UButton
        color="white"
        size="lg"
        icon="i-heroicons-arrow-top-right-on-square-20-solid"
        trailing
        @click="onNewCollection"
      >
        Manage collections
      </UButton>
    </div>

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

    <SampleFilesManager v-model="files" />

    <h2>Submit</h2>

    <div class="flex gap-2 items-center">
      <UButton
        :disabled="!selectedCollectionId"
        :loading="status === 'pending'"
        @click="submitFiles"
      >
        Upload samples
      </UButton>

      <p class="text-red-400 text-sm">
        <span v-if="!selectedCollectionId">
          Select a collection to submit samples to
        </span>
        <span v-else-if="files.length < 1">
          Select at least one file to upload
        </span>
        <span v-if="status === 'error'">
          {{ apiError }}
        </span>
        <span v-if="status === 'success'" class="text-green-400">
          Samples sucessfully submitted
        </span>
      </p>

      <p v-if="!selectedCollectionId" class="text-red-400" />
    </div>
  </main>
</template>

<script lang="ts" setup>
const files = ref<File[]>([])

const selectedCollectionId = ref(null)
function onNewCollection() {
  navigateTo('/collections')
}

const status = ref<'idle' | 'pending' | 'success' | 'error'>(false)
const apiError = ref(null)

function submitFiles() {
  const data = new FormData()
  files.value.forEach(file => data.append('files', file, file.name))
  status.value = 'pending'
  $fetch(`http://127.0.0.1:8000/collections/${selectedCollectionId.value}/datasets`, {
    body: data,
    method: 'post',
  })
    .then(() => {
      status.value = 'success'
    })
    .catch((error) => {
      apiError.value = error
      status.value = 'error'
    })
}

function resetSubmit() {
  status.value = 'idle'
  apiError.value = null
}

watch(selectedCollectionId, resetSubmit)
watch(files, resetSubmit)
</script>
