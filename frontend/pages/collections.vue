<template>
  <main>
    <h1>Collections</h1>
    <UButton class="mb-2" @click="isCreateFormOpen = true">
      New Collection
    </UButton>
    <CollectionsTable :key="refreshKey" />
    <UModal v-model="isCreateFormOpen">
      <CollectionsCreateFormCard @create="onCreate" />
    </UModal>
  </main>
</template>

<script lang="ts" setup>
const isCreateFormOpen = ref(false)
function onCreate() {
  refresh()
  isCreateFormOpen.value = false
}

const refreshKey = ref(1)
function refresh() {
  refreshKey.value += 1
}
</script>
