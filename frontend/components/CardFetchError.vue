<template>
  <UCard>
    <p>Fetch failed</p>
    {{ error }}
  </UCard>
</template>

<script setup lang="ts">
interface Props {
  error: object
}
defineProps<Props>()
</script>
