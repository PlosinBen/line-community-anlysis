<template>
  <div class="my-2 flex flex-col h-full overflow-hidden relative">
    <div class="mx-2 flex items-center">
      <div class="mr-2">
        日期:<select v-model="selectDay" class="border px-2 py-1 rounded ml-2">
          <option v-for="(day, i) in allMessageDay" :key="i">
            {{ day }}
          </option>
        </select>
      </div>
      <div class="mx-2">聊天成員關鍵字: <input v-model="memberName" class="border px-2 py-1 rounded ml-2" /></div>
      <el-button type="success" @click="searchMemberMessages()">顯示</el-button>
    </div>
    <div class="grow px-2 grow overflow-y-scroll relative">
      <div v-if="memberMessages !== null">總計數量: {{ memberMessages.length }}</div>
      <div v-for="(message, i) in memberMessages" :key="i">
        <span class="mx-2 w-20">{{ message.timeText }}</span>
        <span class="mx-2 w-20">{{ message.member }}</span>
        <span class="mx-2">{{ message.message }}</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { IMessage, IParseMessageResult } from '@/types/message'
import { computed, ref, onMounted } from 'vue'

const props = defineProps<{
  data: IParseMessageResult
}>()
const selectDay = ref<string>('')
const memberName = ref<string>('')

const allMessageDay = computed(() => {
  return props.data && props.data.dayMessages.map((d) => d.dayText)
})

const memberMessages = ref<Array<IMessage> | null>(null)
function searchMemberMessages() {
  if (props.data !== null) {
    if (selectDay.value.length > 0 && memberName.value.length > 0) {
      const selectDayMessage = props.data.dayMessages.find((dm) => dm.dayText === selectDay.value)
      if (selectDayMessage) {
        console.log(selectDayMessage.messages)
        memberMessages.value = selectDayMessage.messages.filter((m) => m.member.indexOf(memberName.value) >= 0)
        console.log(memberMessages)
      }
    }
  }
}
</script>

<style scoped></style>
