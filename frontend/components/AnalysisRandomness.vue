<template>
  <details>
    <summary>
      <div class="inline-flex items-center gap-1">
        <Icon
          v-if="isPerfectScore"
          name="i-heroicons-shield-check-solid"
          class="size-6 text-emerald-600"
        />
        <Icon
          v-else
          name="i-heroicons-shield-exclamation-solid"
          class="size-6 text-red-600"
        />
        <p>{{ passedTests.length }} / {{ props.results.length }} randomness tests passed</p>
      </div>
    </summary>
    <ul>
      <li v-for="test in results" :key="test.test_name">
        {{ test.test_name }}: {{ test.passed }}
      </li>
    </ul>
  </details>
</template>

<script lang="ts" setup>
interface TestResult {
  passed: boolean
  test_name: string
}

interface Props {
  results: TestResult[]
}

const props = defineProps<Props>()
const passedTests = computed(() => props.results.filter(r => r.passed === true))
const isPerfectScore = computed(() => {
  return passedTests.value.length === props.results.length
})
</script>
