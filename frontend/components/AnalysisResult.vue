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

      <table class="w-full">
        <tr>
          <td>signal correlation</td>
          <td>{{ dataset.analysis.signal_correlation }}</td>
        </tr>
        <tr>
          <td>after processing</td>
          <td>{{ dataset.analysis.processed_correlation }}</td>
        </tr>
        <tr>
          <td>BDR</td>
          <td>{{ dataset.analysis.quantised_bdr }}</td>
        </tr>
      </table>
    </ucard>
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
