<template>
  <div id="plot" />
</template>

<script lang="ts" setup>
import * as Plotly from 'plotly.js-dist'
import type { Plot } from '~/types/plot'

interface Props {
  plot: Plot
}

const props = defineProps<Props>()

function makeTransparentBackground() {
  // https://github.com/plotly/plotly.js/issues/2006
  document.querySelectorAll('.main-svg').forEach((element) => {
    element.setAttribute('style', 'background: rgba(0, 0, 0, 0);')
  })
  document.querySelectorAll('.modebar-group').forEach((element) => {
    element.setAttribute('style', 'background: rgba(0, 0, 0, 0);')
  })
}

onMounted(() => {
  if (document) {
    Plotly.newPlot('plot', props.plot.data, props.plot.layout)
    makeTransparentBackground()
  }
})
</script>

<style>
.plot-container {
	filter: invert(75%) hue-rotate(180deg);
}
</style>
