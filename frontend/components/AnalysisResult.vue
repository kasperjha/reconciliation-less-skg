<template>
  <div
    v-for="dataset in results"
    :key="dataset.filename"
    class="space-y-2 mb-6"
  >
    <UCard>
      <template #header>
        <h3>{{ dataset.filename }}</h3>
      </template>

      <ul class="list-disc ml-4">
        <li>mismatch count: {{ dataset.mismatch_count }}</li>
        <li>key length: {{ dataset.key_length }}</li>
        <li v-if="dataset.mismatch_count <= 0">
          Secret key: {{ dataset.secret_key }}
        </li>
      </ul>
      <AnalysisRandomness v-if="dataset.randomness.length" :results="dataset.randomness" />
      <p v-else class="mt-2 text-red-600">
        No randomess analysis because of key mismatch
      </p>
    </UCard>
  </div>
</template>

<script setup lang="ts">
import AnalysisRandomness from './AnalysisRandomness.vue'

// TODO: do something to avoid double definition of these types

interface RandomnessResult {
  test_name: string
  passed: boolean
  p_value: number
}

interface AnalysisResultsDataset {
  mismatch_count: number
  key_length: number
  filename: string
  secret_key: string | null
  randomness: RandomnessResult[]
}

interface Props {
  results: AnalysisResultsDataset[]
}
defineProps<Props>()
</script>
