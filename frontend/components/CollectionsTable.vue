<template>
  <UCard v-if="error">
    {{ error }}
  </UCard>
  <ContainerRounded v-else>
    <UTable
      :rows="rows"
      :loading="status === 'loading'"
      :columns="columns"
    />
  </ContainerRounded>
</template>

<script lang="ts" setup>
const { data: collections, status, error } = useFetch('http://127.0.0.1:8000/collections/')

const rows = computed(() => collections.value ? collections.value : [])
const columns = [
  { label: 'ID', key: 'id' },
  { label: 'Name', key: 'name' },
]
</script>
