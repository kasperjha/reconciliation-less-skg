<template>
  <UBreadcrumb divider="/" :links="crumbs" />
</template>

<script lang="ts" setup>
interface Crumb {
  label: string
  to: string
}

function buildCrumbs(routeFullPath: string) {
  const pathParts = routeFullPath.split('/').filter(s => s !== '')
  const reduceFn = (acc: Crumb[], now: string) => {
    const prevCrumb = acc.slice(-1)[0]
    const newCrumb = {
      label: now[0].toUpperCase() + now.slice(1),
      to: acc.length > 1 ? `${prevCrumb.to}/${now}` : `/${now}`,
    }
    return acc.concat([newCrumb])
  }

  const firstCrumb = [{
    label: 'Home',
    to: '/',
  }]

  return pathParts.reduce(reduceFn, firstCrumb)
}

const route = useRoute()
const crumbs = computed(() => buildCrumbs(route.fullPath))
</script>
