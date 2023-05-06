<template>
  <div class="flex flex-col w-full h-full overflow-hidden px-5">
    <div class="text-2xl mb-5 font-bold">上傳檔案進階分析</div>
    <div class="flex items-center">
      <input ref="uploadRef" type="file" class="board p-1 w-60 mr-2" />
      <el-button type="primary" @click="uploadFile">上傳檔案</el-button>
      <!-- <div v-if="isLoading" class="mx-2">讀取中...</div> -->
    </div>
    <router-view></router-view>
  </div>
</template>

<script setup lang="ts">
import { checkFileHeader } from '@/utils/message'
import { ref } from 'vue'
import { router } from '@/router'
import { uploadAnalysisFile } from '@/api/modules/analysis'
const uploadRef = ref<HTMLInputElement>()

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
          if (result.validity) {
            if (result.isIOS) {
              const form = new FormData()
              form.append('file', txtFile)
              const resp = await uploadAnalysisFile(txtFile)
              router.push(`/analysis/${resp.hash}`)
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

<style scoped></style>
