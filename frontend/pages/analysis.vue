<template>
  <main>
    <h1>Analysis</h1>

    <h2>Choose datasets to analyse</h2>
    <CollectionPicker v-model="collectionId" />

    <USelectMenu
      v-model="selectedDatasets"
      :options="rows"
      option-attribute="filename"
      value-attribute="filename"
      placeholder="Select datasets to analyse ..."
      size="lg"
      multiple
    />

    <div class="mt-4 flex gap-2 items-center">
      <UButton @click="onAnalysisClick">
        Analyse
      </UButton>
      <p class="text-red-600">
        <span v-if="selectedDatasets.length < 1">
          Please choose at least one dataset
        </span>
      </p>
    </div>

    <UCard>
      <p>Datasets</p>
      <code><pre>{{ selectedDatasets }}</pre></code>
      <p>collection</p>
      <code><pre>
        {{ collectionId }}
      </pre></code>
    </UCard>

    <h2 class="mt-8">
      Results
    </h2>

    <CardFetchResult :status="status" class="overflow-x-scroll">
      <code>
        <pre>
          {{ analysis.result }}
        </pre>
      </code>
    </CardFetchResult>
  </main>
</template>

<script lang="ts" setup>
const collectionId = ref(null)
const collectionUrl = computed(() => `http://127.0.0.1:8000/collections/${collectionId.value}`)

const { data: datasets } = useFetch(collectionUrl, { immediate: false })
const rows = computed(() => datasets.value ? datasets.value.datasets : [])
const selectedDatasets = ref([])

const { data: analysis, execute, status } = useFetch(`http://127.0.0.1:8000/proto/analysis`, { immediate: false })
function onAnalysisClick() {
  execute()
}
</script>
