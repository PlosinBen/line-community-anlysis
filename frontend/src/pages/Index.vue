<template>
  <div class="flex flex-col w-full h-full overflow-hidden">
    <div class="flex items-center px-5">
      <input ref="uploadRef" type="file" class="board p-1 w-60 mr-2" />
      <el-button type="primary" @click="onReadFile">讀取檔案</el-button>
      <div v-if="parseResult" class="mx-2">
        功能選擇:
        <select v-model="functionSelect" class="border px-2 py-1 rounded ml-2">
          <option>每日訊息統計</option>
          <!-- <option>單日訊息統計</option> -->
          <option>查詢賢達訊息</option>
        </select>
      </div>
    </div>
    <div v-if="parseResult" class="grow h-full overflow-hidden">
      <all-day-count v-if="functionSelect === '每日訊息統計'" :data="parseResult"></all-day-count>
      <search-member-message v-if="functionSelect === '查詢賢達訊息'" :data="parseResult"></search-member-message>
    </div>
  </div>
</template>

<script lang="ts" setup>
import type { IParseMessageResult } from '@/types/message'
import { ref } from 'vue'
import { parserMessage } from '@/utils/message'
import AllDayCount from './home/AllDayCount.vue'
import SearchMemberMessage from './home/SearchMemberMessage.vue'

const uploadRef = ref<HTMLInputElement>()
const parseResult = ref<IParseMessageResult | null>(null)

const functionSelect = ref<string>('每日訊息統計')

const allMessageString = ref<string>('')

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
          const lines = fileContent.split('\n').filter((line) => line.length !== 0)
          parseResult.value = parserMessage(lines)
        }
      }
      reader.readAsText(txtFile)
    }
  }
}
</script>

<style lang="scss"></style>
