<template>
  <canvas ref="canvasRef"></canvas>
  <!-- <div class="w-3/4"> -->
  <!-- </div> -->
</template>

<script setup lang="ts">
import { computed, ref, onMounted } from 'vue'
import Chart from 'chart.js/auto'
import { ICountFilterOption, IParseMessageResult } from '@/types/message'
import { countMessageByDay } from '@/utils/message'

const props = defineProps<{
  data: IParseMessageResult
  filter: ICountFilterOption
}>()

const canvasRef = ref<HTMLCanvasElement>()
const chart = ref<Chart>()

function draw() {
  if (chart.value) {
    chart.value.destroy()
  }
  if (canvasRef.value) {
    const countDay = countMessageByDay(props.data, props.filter)
    chart.value = new Chart(canvasRef.value, {
      type: 'bar',
      data: {
        datasets: [{ label: '每日訊息數', data: countDay.map((cd) => cd.count) }],
        labels: countDay.map((cd) => cd.day),
      },
    })
  }
}
onMounted(() => {
  // draw()
})
defineExpose({ draw })
</script>

<style scoped></style>
