<template>
  <UCard>
    <slot v-if="status === 'idle'" name="idle">
      <div class="flex items-center justify-center gap-2">
        <Icon name="i-heroicons-exclamation-circle-20-solid" class="size-5" />
        <p>Waiting to load from API</p>
      </div>
    </slot>

    <slot v-else-if="status === 'pending'" name="idle">
      <div class="flex items-center justify-center gap-2">
        <Icon name="i-heroicons-arrow-path-20" class="size-5" />
        <p>API response is loading</p>
      </div>
    </slot>

    <slot v-else-if="status === 'error'" name="error">
      <div class="flex items-center justify-center gap-2">
        <Icon name="i-heroicons-arrow-path-20" class="size-5" />
        <p>Error loading API response</p>
      </div>
    </slot>

    <slot v-else-if="status === 'success'" name="default">
      <div class="flex items-center justify-center gap-2">
        <Icon name="i-heroicons-check-circle-20-solid" class="size-5" />
        <p>API response loaded successfully</p>
      </div>
    </slot>
  </UCard>
</template>

<script lang="ts" setup>
defineProps<Props>()

interface Props {
  status: 'idle' | 'pending' | 'success' | 'error'
}
</script>
