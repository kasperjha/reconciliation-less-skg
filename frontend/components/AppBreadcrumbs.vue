<template>
  <UBreadcrumb divider="/" :links="crumbs" />
</template>

<script lang="ts" setup>
function makeCrumb(prevUrl: string, thisPath: string) {
  return {
    label: thisPath[0].toUpperCase() + thisPath.slice(1),
    to: `${prevUrl}/${thisPath}`,
  }
}

function buildCrumbs(routeFullPath: string) {
  const homeCrumb = {
    label: 'Home',
    to: '/',
  }
  const pathParts = routeFullPath.split('/')
  const restCrumbs = pathParts.filter(s => s !== '').reduce((prev, now) => prev.concat([makeCrumb(prev.slice(-1)[0].label, now)]), [{ to: '', label: '' }])
  return [homeCrumb].concat(restCrumbs.slice(1))
}

const route = useRoute()
const crumbs = computed(() => buildCrumbs(route.fullPath))
</script>
