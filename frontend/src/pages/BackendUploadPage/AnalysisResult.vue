<template>
  <div v-if="analysisResult" class="grow h-full overflow-hidden pt-5">
    <div>
      <el-button type="success" :icon="Share" @click="shareToLine">分享到Line</el-button>
    </div>
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
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { getAnalysisResult } from '@/api/modules/analysis'
import { Share } from '@element-plus/icons-vue'

const props = defineProps<{ hash: string }>()
const analysisResult = ref<{
  analysis: { [key: string]: any }
} | null>(null)

const shareToLine = () => {
  const url = `https://social-plugins.line.me/lineit/share?url=${location.href}`
  window.open(url, '_blank')
}

onMounted(async () => {
  analysisResult.value = await getAnalysisResult(props.hash)
})
</script>

<style scoped></style>
