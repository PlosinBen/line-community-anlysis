<template>
  <div class="w-full">
    基本資訊
    <div>總訊息數: {{ allDayMessage.length }}</div>
    <div>記錄檔起訖時間: {{ startEndTime }}</div>
    <div>記錄檔統計日數: {{ totalDays }}</div>
    <div>平均每日訊息數: {{ arvgMessagePreDay.toFixed(2) }}</div>
  </div>
</template>

<script setup lang="ts">
import { IParseMessageResult } from '@/types/message'
import { concatAllDaysMessages } from '@/utils/message'
import moment from 'moment'
import { computed } from 'vue'

const props = defineProps<{
  data: IParseMessageResult
}>()

const allDayMessage = computed(() => {
  return concatAllDaysMessages(props.data.dayMessages)
})

const startEndTime = computed(() => {
  if (allDayMessage.value.length === 0) return ''
  const firstMsg = allDayMessage.value[0]
  const lastMsg = allDayMessage.value.at(-1)
  return `${moment(firstMsg.timestamp).format('YYYY-MM-DD HH:mm')}~${moment(lastMsg?.timestamp).format('YYYY-MM-DD HH:mm')}`
})

const totalDays = computed(() => {
  const startDay = moment(props.data.dayMessages[0].timestamp)
  const endDay = moment(props.data.dayMessages.at(-1)?.timestamp)
  const diffDay = endDay.diff(startDay, 'day')
  return diffDay
})

const arvgMessagePreDay = computed(() => {
  return allDayMessage.value.length / totalDays.value
})
</script>

<style scoped></style>
