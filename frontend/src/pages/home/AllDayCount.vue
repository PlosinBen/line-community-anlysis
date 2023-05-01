<template>
  <div class="flex flex-col h-full overflow-y-auto relative">
    <div class="flex">
      <div class="mx-2">
        <label v-for="option in filterOptions" :key="option.key" class="block">
          {{ option.label }}
          <input v-model="filterSetting[option.key]" type="checkbox" />
        </label>
      </div>
      <div class="mx-2">
        <el-button type="success" @click="dayCountChartRef?.draw()">圖表繪製</el-button>
      </div>
    </div>
    <div v-if="props.data" class="grow h-full">
      <day-count-chart ref="dayCountChartRef" :data="props.data" :filter="filterSetting"></day-count-chart>
    </div>
  </div>
</template>

<script setup lang="ts">
import DayCountChart from '@/components/DayCountChart.vue'
import { ICountFilterOption, IParseMessageResult } from '@/types/message'
import { ref } from 'vue'

const props = defineProps<{
  data: IParseMessageResult
}>()
const dayCountChartRef = ref<InstanceType<typeof DayCountChart>>()

const filterSetting = ref<ICountFilterOption>({
  chartRoomSetting: false,
  forceRemoveMember: false,
  joinOrLeaveGroup: false,
  autoReplyMessage: false,
  systemForceRemoveMessage: false,
  revokeMessage: false,
  stickerMessage: false,
  photoMessage: false,
  videoMessage: false,
  generalMessage: true,
})

const filterOptions = [
  { label: '群組設定', key: 'chartRoomSetting' },
  { label: '強制移除成員', key: 'forceRemoveMember' },
  { label: '成員加入/離開', key: 'joinOrLeaveGroup' },
  { label: '自動回應訊息', key: 'autoReplyMessage' },
  { label: '系統回收訊息', key: 'systemForceRemoveMessage' },
  { label: '回收訊息', key: 'revokeMessage' },
  { label: '貼圖訊息', key: 'stickerMessage' },
  { label: '照片訊息', key: 'photoMessage' },
  { label: '影片訊息', key: 'videoMessage' },
  { label: '一般聊天訊息', key: 'generalMessage' },
]
</script>

<style scoped></style>
