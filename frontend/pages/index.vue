<template>
  <div>
    <h1>SKG Analysis Framework</h1>
    <div class="grid grid-cols-3 gap-2 h-40 items-stretch">
      <CardChoice
        v-for="action in heroPageActions"
        :key="action.to"
        v-bind="action"
      />
    </div>
  </div>
</template>

<script lang="ts" setup>
interface Action {
  title: string
  description?: string
  to: string
}

const heroPageActions: Action[] = [
  { title: '1. Ingest', description: 'Load and prepare RSSI samples.', to: '/ingestion' },
  { title: '2. Manage', description: 'Manage collections of ingested RSSI samples.', to: '/collections' },
  { title: '3. Analyse', description: 'Investigate the applicability of SKG for collected data.', to: '/analysis' },
]
</script>
