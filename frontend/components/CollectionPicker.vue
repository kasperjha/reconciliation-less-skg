<template>
  <CardFetchError v-if="error" :error="error" />
  <USelectMenu
    v-else
    v-model="model"
    option-attribute="name"
    value-attribute="id"
    :disabled="isDisabled"
    :loading="status === 'pending'"
    placeholder="Select collection ..."
    size="lg"
    :options
  />
</template>

<script lang="ts" setup>
const model = defineModel()

interface Collection {
  id: number
  name: string
}

const { data, status, error } = useFetch<Collection[]>('http://127.0.0.1:8000/collections/')

const options = computed(() => {
  return data.value ? data.value : []
})

const isDisabled = computed(() => {
  return status.value === 'error' || status.value === 'pending'
})
</script>
