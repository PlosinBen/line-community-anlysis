<template>
  <div class="flex flex-col">
    <div>
      <input ref="uploadRef" type="file" class="board p-1 w-60 mr-2" />
      <el-button type="primary" @click="onReadFile">讀取檔案</el-button>
    </div>
    <div v-if="parseResult" class="flex flex-col my-2">
      <div class="my-2 flex">
        <div class="mx-2">
          功能選擇:
          <select v-model="functionSelect" class="border px-2 py-1 rounded ml-2">
            <option>每日訊息統計</option>
          </select>
        </div>
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
    </div>
    <div v-if="false" class="flex flex-col my-2">
      <div class="my-2">
        日期:<select class="border px-2 py-1 rounded ml-2">
          <option v-for="(day, i) in allMessageDay" :key="i">
            {{ day }}
          </option>
        </select>
      </div>
      <div class="my-2">
        聊天成員清單:
        <select class="border px-2 py-1 rounded ml-2">
          <option v-for="(member, i) in allMembers" :key="i">
            {{ member }}
          </option>
        </select>
      </div>
    </div>
    <div v-if="parseResult" class="flex flex-col my-2">
      <day-count-chart ref="dayCountChartRef" :data="parseResult" :filter="filterSetting"></day-count-chart>
    </div>
  </div>
  <!-- <img alt="Vue logo" src="@/assets/images/logo.png" class="w-30" /> -->
  <!-- <HelloWorld :msg="t('common.hello')" /> -->
  <!-- <VueUse /> -->
</template>

<script lang="ts" setup>
import type { IParseMessageResult, ICountFilterOption } from '@/types/message'
import { computed, ref } from 'vue'
import { parserMessage } from '@/utils/message'
import DayCountChart from '@/components/DayCountChart.vue'
// import type { UploadInstance } from 'element-plus'

const uploadRef = ref<HTMLInputElement>()
const dayCountChartRef = ref<InstanceType<typeof DayCountChart>>()
const parseResult = ref<IParseMessageResult | null>(null)

const functionSelect = ref<string>('每日訊息統計')

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

const allMessageString = ref<string>('')

const allMessageDay = computed(() => {
  return parseResult.value && parseResult.value.dayMessages.map((d) => d.dayText)
})

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
