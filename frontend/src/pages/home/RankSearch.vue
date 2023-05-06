<template>
  <div class="mx-2 my-3">
    排行查詢:
    <select v-model="selectFilter" class="border px-2 py-1 rounded ml-2">
      <option v-for="option in filterOptions" :key="option.key" :value="option.key">{{ option.label }}</option>
    </select>
    <el-button class="mx-2" type="primary" @click="search">顯示</el-button>
  </div>
  <div calss="my-3">
    <table class="table">
      <thead>
        <tr>
          <th>名稱</th>
          <th>數量</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in resultData" :key="item.user">
          <td>{{ item.user }}</td>
          <td>{{ item.count }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup lang="ts">
import { ICountFilterOption, IParseMessageResult } from '@/types/message'
import { concatAllDaysMessages, countMessagesByUser, filterMessage } from '@/utils/message'
import { computed, ref } from 'vue'

const props = defineProps<{
  data: IParseMessageResult
}>()

const allDayMessage = computed(() => {
  return concatAllDaysMessages(props.data.dayMessages)
})

const selectFilter = ref('systemForceRemoveMessage')

const filterOptions = [
  { label: '系統回收訊息', key: 'systemForceRemoveMessage' },
  { label: '回收訊息', key: 'revokeMessage' },
  { label: '貼圖訊息', key: 'stickerMessage' },
  { label: '照片訊息', key: 'photoMessage' },
  { label: '影片訊息', key: 'videoMessage' },
  { label: '一般聊天訊息', key: 'generalMessage' },
]

const resultData = ref<Array<{ user: string; count: number }> | null>(null)

const search = () => {
  const allTargetMessage = filterMessage(allDayMessage.value, { [selectFilter.value]: true })
  // console.log(allTargetMessage)
  const result = countMessagesByUser(allTargetMessage)
  resultData.value = result.slice(0, 10)
  console.log(result)
}
</script>

<style scoped></style>
