<template>
  <div>
    <h1>SKG Analysis Framework</h1>
    <div class="grid grid-cols-3 gap-2 h-40 items-stretch">
      <ButtonCard
        v-for="action in heroPageActions"
        :key="action.url"
        :to="action.url"
        class="w-full h-full"
      >
        {{ action.label }}
      </ButtonCard>
    </div>
  </div>
</template>

<script lang="ts" setup>
interface LabeledLink {
  label: string
  url: string
}
const heroPageActions: LabeledLink[] = [
  { label: 'Analysis', url: '/analysis' },
  { label: 'Ingestion', url: '/ingestion' },
  { label: 'Collections', url: '/collections' },
]
</script>
