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
        New collection
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
  </main>
</template>

<script lang="ts" setup>
const files = ref<File[]>([])

const selectedCollectionId = ref(null)
function onNewCollection() {
  navigateTo('/collections')
}
</script>
