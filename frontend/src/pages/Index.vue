<template>
  <div class="flex flex-col overflow-hidden">
    <div class="flex items-center">
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
  <!-- <img alt="Vue logo" src="@/assets/images/logo.png" class="w-30" /> -->
  <!-- <HelloWorld :msg="t('common.hello')" /> -->
  <!-- <VueUse /> -->
</template>

<script lang="ts" setup>
import type { IParseMessageResult, ICountFilterOption, IMessage } from '@/types/message'
import { computed, ref } from 'vue'
import { parserMessage } from '@/utils/message'
import AllDayCount from './home/AllDayCount.vue'
import SearchMemberMessage from './home/SearchMemberMessage.vue'
import DayCountChart from '@/components/DayCountChart.vue'
// import type { UploadInstance } from 'element-plus'

const uploadRef = ref<HTMLInputElement>()
const dayCountChartRef = ref<InstanceType<typeof DayCountChart>>()
const parseResult = ref<IParseMessageResult | null>(null)

const functionSelect = ref<string>('每日訊息統計')

const allMessageString = ref<string>('')

const allMembers = computed(() => {
  let result = null
  if (parseResult.value) {
    result = Array.from(parseResult.value.userSets)
    result.sort((a, b) => a.localeCompare(b))
  }
  return result
})

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
          // console.log(lines)
          parseResult.value = parserMessage(lines)
          // parserMessage(lines)
        }
      }
      reader.readAsText(txtFile)
    }
  }
}
// import { useI18n } from 'vue-i18n'
// import HelloWorld from '@/components/HelloWorld.vue'
// import VueUse from '@/components/VueUse.vue'

// const { t } = useI18n()
</script>

<style lang="scss"></style>
