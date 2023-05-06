<template>
  <div class="flex flex-col w-full h-full overflow-hidden px-5">
    <div class="text-2xl mb-5 font-bold">風險評價計算</div>
    <div class="w-80">
      <div>
        <el-date-picker
          v-model="dateRange"
          type="daterange"
          range-separator="至"
          start-placeholder="開始日期"
          end-placeholder="結束日期"
          :size="'default'"
        />
        <div class="py-2">
          標的代號:
          <el-input v-model="assetInput" placeholder="請輸入標的代號，並用逗號區隔，ex: QQQ,SPY" />
        </div>
        <div class="py-2">
          計算週期:
          <el-input v-model="periodInput" placeholder="請輸入計算週期，並用逗號區隔，ex:8,10,200" />
        </div>
        <div class="py-2">
          <el-button type="primary" @click="query">查詢</el-button>
        </div>
      </div>
    </div>
    <div v-if="currentResult" class="w-120">
      <table class="table table-bordered">
        <thead>
          <tr>
            <th rowspan="2" style="vertical-align: middle; text-align: center">標的代號</th>
            <th :colspan="currPeriods.length" style="vertical-align: middle; text-align: center">計算週期</th>
          </tr>
          <tr>
            <th v-for="(period, i) in currPeriods" :key="i" style="vertical-align: middle; text-align: center">{{ period }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(asset, i) in currAssets" :key="i">
            <td style="vertical-align: middle; text-align: center">{{ asset }}</td>
            <td v-for="(period, j) in currPeriods" :key="j" style="vertical-align: middle; text-align: right">
              {{ currentResult[period][asset] }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup lang="ts">
import moment from 'moment'
import { ref } from 'vue'
import { getRisk } from '@/api/modules/risk'

const dateRange = ref('')
const assetInput = ref('')
const periodInput = ref('')

const currPeriods = ref<Array<string>>([])
const currAssets = ref<Array<string>>([])

const currentResult = ref<Record<string, any>>()

const query = async () => {
  const [start, end] = dateRange.value
  const [start_date, end_date] = [moment(start), moment(end)]
  console.log(start_date.format('YYYY-MM-DD'), end_date.format('YYYY-MM-DD'))
  currAssets.value = assetInput.value.split(',')
  currPeriods.value = periodInput.value.split(',')
  currentResult.value = await getRisk(start_date.format('YYYY-MM-DD'), end_date.format('YYYY-MM-DD'), currAssets.value, currPeriods.value)
}
</script>

<style scoped></style>
