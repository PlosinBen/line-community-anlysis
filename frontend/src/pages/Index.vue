<template>
  <div class="flex flex-col w-full h-full overflow-hidden">
    <div class="flex items-center px-5">
      <input ref="uploadRef" type="file" class="board p-1 w-60 mr-2" />
      <el-button type="primary" @click="uploadFile">上傳檔案</el-button>
      <el-button type="primary" @click="onReadFile">讀取檔案</el-button>
      <div v-if="isLoading">讀取中...</div>
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
    <div v-if="analysisResult" class="grow h-full overflow-hidden">
      <div>總發言量: {{ analysisResult.analysis['number_of_message'] }}</div>
      <div>發言過的人數: {{ analysisResult.analysis['number_of_spoken_user'] }}</div>
      <div>系統訊息數: {{ analysisResult.analysis['number_of_sys_message'] }}</div>
      <div>使用者訊息數: {{ analysisResult.analysis['number_of_user_message'] }}</div>
      <div>
        <div class="my-3">
          使用者訊息排名<br />
          <table class="border">
            <tr>
              <th class="border">名稱</th>
              <th class="border">訊息數</th>
            </tr>
            <tr v-for="(item, i) in analysisResult.analysis['ranking_of_user_message']" :key="i">
              <td class="border">{{ item[0] }}</td>
              <td class="border">{{ item[1] }}</td>
            </tr>
          </table>
        </div>
        <div class="my-3">
          使用貼圖排名<br />
          <table class="border">
            <tr>
              <th class="border">名稱</th>
              <th class="border">貼圖數</th>
            </tr>
            <tr v-for="(item, i) in analysisResult.analysis['ranking_of_user_sticker']" :key="i">
              <td class="border">{{ item[0] }}</td>
              <td class="border">{{ item[1] }}</td>
            </tr>
          </table>
        </div>
      </div>
    </div>
    <div v-if="parseResult" class="grow h-full overflow-hidden">
      <base-info v-if="functionSelect === '基本統計資訊'" :data="parseResult"></base-info>
      <all-day-count v-if="functionSelect === '每日訊息統計圖表'" :data="parseResult"></all-day-count>
      <rank-search v-if="functionSelect === '排行查詢'" :data="parseResult"></rank-search>
      <search-member-message v-if="functionSelect === '查詢賢達訊息'" :data="parseResult"></search-member-message>
    </div>
  </div>
</template>

<script lang="ts" setup>
import type { IParseMessageResult } from '@/types/message'
import { ref } from 'vue'
import { sleep, parserMessage, checkFileHeader } from '@/utils/message'
import request from '@/utils/axios'
import AllDayCount from './home/AllDayCount.vue'
import SearchMemberMessage from './home/SearchMemberMessage.vue'
import BaseInfo from './home/BaseInfo.vue'
import RankSearch from './home/RankSearch.vue'

const uploadRef = ref<HTMLInputElement>()
const parseResult = ref<IParseMessageResult | null>(null)

const functionSelect = ref<string>('基本統計資訊')

const isLoading = ref<boolean>(false)
const persent = ref<string>('')

const allMessageString = ref<string>('')
const analysisResult = ref<{
  analysis: { [key: string]: any }
} | null>(null)

const onReadFile = () => {
  const files = uploadRef.value?.files
  if (files && files.length > 0) {
    const txtFile = files[0]
    if (!txtFile.type.startsWith('text/')) {
      alert('請選擇文字檔案')
      return
    } else {
      const reader = new FileReader()
      reader.onload = async (event) => {
        await sleep(0.001)
        const fileContent = event.target?.result
        if (fileContent && typeof fileContent === 'string') {
          const lines = fileContent.split(/\r?\n/).filter((line) => line.length !== 0)
          parseResult.value = await parserMessage(lines, (p) => {
            persent.value = p
            // console.log(p)
          })
        }
        isLoading.value = false
      }
      isLoading.value = true
      reader.readAsText(txtFile)
    }
  }
}

const uploadFile = async () => {
  const files = uploadRef.value?.files
  if (files && files.length > 0) {
    const txtFile = files[0]
    if (!txtFile.type.startsWith('text/')) {
      alert('請選擇文字檔案')
      return
    } else {
      const reader = new FileReader()
      reader.onload = async (event) => {
        const fileContent = event.target?.result
        if (fileContent && typeof fileContent === 'string') {
          const lines = fileContent.split('\n').filter((line) => line.length !== 0)
          const result = checkFileHeader(lines[0])
          console.log(result)
          if (result.validity) {
            if (result.isIOS) {
              const form = new FormData()
              form.append('file', txtFile)
              const resp = await request.post<{ hash: string }>('/api/line_community_analysis', form)
              analysisResult.value = await request.get(`/api/line_community_analysis/${resp.hash}`)
              console.log(analysisResult.value)
            } else {
              alert('目前僅支援 iOS 匯出檔案上傳')
            }
          } else {
            alert('請使用未調整過的 LINE 匯出檔案')
          }
        }
      }
      reader.readAsText(txtFile)
    }
  }
}
</script>

<style lang="scss"></style>
