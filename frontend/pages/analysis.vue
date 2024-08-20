<template>
  <main>
    <h1>Analysis</h1>

    <h2>Choose collection to analyse</h2>

    <div class="flex gap-1">
      <CollectionPicker v-model="collectionId" class="flex-grow" />
      <UButton
        color="white"
        size="lg"
        icon="i-heroicons-arrow-top-right-on-square-20-solid"
        trailing
        @click="navigateTo('/collections')"
      >
        Manage collections
      </UButton>
    </div>

    <ContainerRounded class="mt-2">
      <div v-if="validationError" class="text-gray-600 h-40 flex justify-center gap-1 items-center">
        <Icon name="i-heroicons-shield-exclamation" class="size-5" />
        <p>{{ validationError }}</p>
      </div>
      <UTable v-else :rows="datasets" />
    </ContainerRounded>

    <UButton
      :disabled="validationError !== null"
      size="md"
      @click="onAnalysisClick"
    >
      Analyse
    </UButton>

    <h2>Results</h2>

    <AnalysisResult v-if="analysis" :results="analysis.results" />

    <UCard v-if="analysis">
      <details>
        <summary>Raw analysis data</summary>
        <code><pre>{{ analysis }}</pre></code>
      </details>
    </UCard>
  </main>
</template>

<script lang="ts" setup>
const collectionId = ref(null)
const collectionUrl = computed(() => `http://127.0.0.1:8000/collections/${collectionId.value}`)

const { data: collection } = useFetch(collectionUrl, { immediate: false })
const datasets = computed(() => collection.value !== null ? collection.value.datasets : [])

const validationError = computed<string | null>(() => {
  if (datasets.value.length < 1) {
    return 'Select a collection with at least one dataset'
  }
  else {
    return null
  }
})

const analysis = ref<null | object>(null)
const analysisUrl = computed(() => `http://127.0.0.1:8000/collections/${collectionId.value}/analyse`)

function onAnalysisClick() {
  $fetch<object>(analysisUrl.value, { method: 'POST' })
    .then(data => analysis.value = data)
    .catch(error => console.log(error))
}
</script>
