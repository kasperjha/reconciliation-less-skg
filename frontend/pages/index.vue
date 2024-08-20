<template>
  <main>
    <h1>SKG Analysis Framework</h1>
    <div class="grid grid-cols-3 gap-2 h-40 items-stretch">
      <CardChoice
        v-for="action in heroPageActions"
        :key="action.to"
        v-bind="action"
      />
    </div>
  </main>
</template>

<script lang="ts" setup>
interface Action {
  title: string
  description?: string
  to: string
  disabled?: boolean
}

const heroPageActions: Action[] = [
  { title: 'Ingest', description: 'Load and prepare RSSI samples.', to: '/ingestion', disabled: false },
  { title: 'Manage', description: 'Manage collections of ingested RSSI samples.', to: '/collections', disabled: false },
  { title: 'Analysis', description: 'Investigate the applicability of SKG for collected data.', to: '/analysis', disabled: false },
]
</script>
