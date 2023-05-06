<template>
  <div class="flex flex-col w-full h-full overflow-hidden px-5">
    <div class="text-2xl mb-5 font-bold">前端讀檔分析功能</div>
    <div class="flex items-center">
      <input ref="uploadRef" type="file" class="board p-1 w-60 mr-2" />
      <el-button type="primary" @click="onReadFile">讀取檔案</el-button>
      <div v-if="isLoading" class="mx-2">讀取中...</div>
      <div v-if="parseResult" class="mx-2">
        功能選擇:
        <select v-model="functionSelect" class="border px-2 py-1 rounded ml-2">
          <option>基本統計資訊</option>
          <option>每日訊息統計圖表</option>
          <option>排行查詢</option>
          <!-- <option>單日訊息統計</option> -->
          <option>查詢賢達訊息</option>
        </select>
      </div>
    </div>
    <div v-if="parseResult" class="grow h-full overflow-hidden pt-5">
      <base-info v-if="functionSelect === '基本統計資訊'" :data="parseResult"></base-info>
      <all-day-count v-if="functionSelect === '每日訊息統計圖表'" :data="parseResult"></all-day-count>
      <rank-search v-if="functionSelect === '排行查詢'" :data="parseResult"></rank-search>
      <search-member-message v-if="functionSelect === '查詢賢達訊息'" :data="parseResult"></search-member-message>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { IParseMessageResult } from '@/types/message'
import { parserMessage } from '@/utils/message'

import AllDayCount from './AllDayCount.vue'
import SearchMemberMessage from './SearchMemberMessage.vue'
import BaseInfo from './BaseInfo.vue'
import RankSearch from './RankSearch.vue'

const uploadRef = ref<HTMLInputElement>()

const parseResult = ref<IParseMessageResult | null>(null)
const isLoading = ref<boolean>(false)
const functionSelect = ref<string>('基本統計資訊')

const onReadFile = () => {
  const files = uploadRef.value?.files
  if (files && files.length > 0) {
    const txtFile = files[0]
    if (!txtFile.type.startsWith('text/')) {
      alert('請選擇文字檔案')
      return
    } else {
      const reader = new FileReader()
      reader.onload = (event) => {
        const fileContent = event.target?.result
        if (fileContent && typeof fileContent === 'string') {
          const lines = fileContent.split(/\r?\n/).filter((line) => line.length !== 0)
          parseResult.value = parserMessage(lines)
        }
        isLoading.value = false
      }
      isLoading.value = true
      reader.readAsText(txtFile)
    }
  }
}
</script>

<style scoped></style>
