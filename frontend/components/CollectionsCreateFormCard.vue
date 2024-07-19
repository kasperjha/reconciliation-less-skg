<template>
  <form action="" @submit.prevent="onSubmit()">
    <UCard>
      <template #header>
        <p class="text-lg">
          Create new collection
        </p>
      </template>

      <label for="collection-name" class="text-gray-600">Collection name</label>
      <UInput
        id="collection-name"
        v-model="collectionName"
        type="text"
        class="mt-2"
        required
        placeholder="New collection"
      />
      <template #footer>
        <UButton type="submit" :loading="status === 'loading'">
          Create collection
        </UButton>
      </template>
    </UCard>
  </form>
</template>

<script lang="ts" setup>
const emit = defineEmits(['create'])

const collectionName = ref<string | null>()

const body = computed(() => ({
  name: collectionName.value,
}))

const { status, execute } = useFetch('http://127.0.0.1:8000/collections/', {
  method: 'POST',
  body,
  watch: false,
  immediate: false,
})

function onSubmit() {
  execute().then(() => emit('create'))
}
</script>
