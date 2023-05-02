import moment from 'moment'
// import createJieba from 'js-jieba'
// import { JiebaDict, HMMModel, UserDict, IDF, StopWords } from 'jieba-zh-tw'
import { type ICountFilterOption, type IDayMessages, type IMessage, type IParseMessageResult } from '@/types/message'

// const jieba = createJieba(JiebaDict, HMMModel, UserDict, IDF, StopWords)
enum eMessageType {
  ChatRoomSetting = 'ChatRoomSetting',
  ForceRemoveMember = 'ForceRemoveMember',
  MemberJoinOrLeaveGroup = 'MemberJoinOrLeaveGroup',
  AutoReplyMessage = 'AutoReplyMessage',
  SystemForceRemoveMessage = 'SystemForceRemoveMessage',
  RevokeMessage = 'RevokeMessage',
  StickerMessage = 'StickerMessage',
  PhotoMessage = 'PhotoMessage',
  VideoMessage = 'VideoMessage',
  GeneralMessage = 'GeneralMessage',
}

export function parserMessage(rawData: string[]): IParseMessageResult {
  const dataLength = rawData.length
  const test = rawData.slice(0, 100)
  const title = test[0]
  const storeAt = rawData[1]

  const userSets = new Set<string>()
  const dayMessages: Array<IDayMessages> = []
  let firstDate = (/^(\d{4}\/\d{1,2}\/\d{1,2})[\w|\W]*/.exec(rawData[2]) as RegExpExecArray)[1]
  dayMessages.push({
    timestamp: moment(`${firstDate.replace(/\//g, '-')} 00:00:00`).valueOf(),
    dayText: firstDate,
    messages: [],
  })
  let i = 3
  console.time('parser message')
  while (i < dataLength) {
    const currentMsg = rawData[i]
    let currentRule
    for (let j = 0; j < messageRegex.length; j++) {
      if (messageRegex[j].regex.test(currentMsg)) {
        currentRule = messageRegex[j]
        break
      }
    }
    try {
      if (currentRule) {
        const regexArray = currentRule.regex.exec(currentMsg) as RegExpExecArray
        const [, time, member, message] = regexArray
        let currentMsgType = eMessageType.GeneralMessage
        if (currentRule.name === 'Change Date') {
          firstDate = regexArray[1]
          dayMessages.push({
            timestamp: moment(firstDate).startOf('day').valueOf(),
            dayText: firstDate,
            messages: [],
          })
        } else {
          if (currentRule.name === 'Chat Room Setting') {
            currentMsgType = eMessageType.ChatRoomSetting
          } else if (currentRule.name === 'Force Remove Member') {
            currentMsgType = eMessageType.ForceRemoveMember
          } else if (currentRule.name === 'Member Join/Leave Group') {
            currentMsgType = eMessageType.MemberJoinOrLeaveGroup
          } else if (currentRule.name === 'Auto Reply Message') {
            currentMsgType = eMessageType.AutoReplyMessage
          } else if (currentRule.name === 'System Force Remove Message') {
            currentMsgType = eMessageType.SystemForceRemoveMessage
          } else if (currentRule.name === 'Revoke Message') {
            currentMsgType = eMessageType.RevokeMessage
          } else if (currentRule.name === 'Sticker Message') {
            currentMsgType = eMessageType.StickerMessage
          } else if (currentRule.name === 'Photo Message') {
            currentMsgType = eMessageType.PhotoMessage
          } else if (currentRule.name === 'Video Message') {
            currentMsgType = eMessageType.VideoMessage
          }
          userSets.add(member)
          if (dayMessages.length > 0) {
            dayMessages.at(-1)?.messages.push({
              timestamp: moment(`${firstDate} ${time}`).startOf('minute').valueOf(),
              timeText: time,
              messageType: currentMsgType,
              member,
              message,
            })
          }
        }
      } else {
        if (dayMessages.length > 0) {
          const currentDayMessage = dayMessages.at(-1) as IDayMessages
          ;(currentDayMessage.messages.at(-1) as IMessage).message += `\n${currentMsg}`
        }
      }
    } catch {
      console.log(currentMsg)
      console.log(currentRule?.name)
    }
    i++
    // console.log(i)
  }
  console.log(userSets)
  console.log(dayMessages)
  console.timeEnd('parser message')

  // console.log(test)
  // const messages = test.map((line) => {
  //   const currentRule = messageRegex.find((rule) => rule.regex.test(line))
  //   if (currentRule) {
  //     console.log(currentRule.name)
  //     return currentRule.regex.exec(line)
  //   } else {
  //     console.log('not match')
  //     return []
  //   }
  // })
  // console.log(messages)

  return {
    title,
    storeAt,
    userSets,
    dayMessages,
  }
}

export function parserMessageAsync(rawData: string[]): Promise<IParseMessageResult> {
  return new Promise((resolve, reject) => {
    try {
      resolve(parserMessage(rawData))
    } catch (e) {
      reject(e)
    }
  })
}

const messageRegex = [
  {
    name: 'Change Date',
    regex: /^(\d{4}\/\d{1,2}\/\d{1,2})(（週\S）)/,
  },
  {
    name: 'Chat Room Setting',
    // eslint-disable-next-line
    regex: /^(\d{2}\:\d{2})\t(.+)(已將聊天室的人數上限設為\d+人|變更了聊天室圖片)/,
  },
  {
    name: 'Force Remove Member',
    // eslint-disable-next-line
    regex: /^(\d{2}\:\d{2})\t(.+)(已將.+強制退出社群。)/,
  },
  {
    name: 'Member Join/Leave Group',
    // eslint-disable-next-line
    regex: /^(\d{2}\:\d{2})\t(.+)(加入聊天|離開聊天)/,
  },
  {
    name: 'Auto Reply Message',
    // eslint-disable-next-line
    regex: /^(\d{2}\:\d{2})\t(Auto-reply)\t(.+)/,
  },
  {
    name: 'System Force Remove Message',
    // eslint-disable-next-line
    regex: /^(\d{2}\:\d{2})\t(.+)(的訊息可能已違反社群服務條款而遭刪除。)/,
  },
  {
    name: 'Revoke Message',
    // eslint-disable-next-line
    regex: /^(\d{2}\:\d{2})\t(.+)(已收回訊息)/,
  },
  {
    name: 'Sticker Message',
    // eslint-disable-next-line
    regex: /^(\d{2}\:\d{2})\t(.+)\t(\[貼圖\])/,
  },
  {
    name: 'Photo Message',
    // eslint-disable-next-line
    regex: /^(\d{2}\:\d{2})\t(.+)\t(\[照片\])/,
  },
  {
    name: 'Video Message',
    // eslint-disable-next-line
    regex: /^(\d{2}\:\d{2})\t(.+)\t(\[影片\])/,
  },
  {
    name: 'General Message',
    // eslint-disable-next-line
    regex: /^(\d{2}\:\d{2})\t(.+)\t(.+)/,
  },
]

export function countMessageByDay(data: IParseMessageResult, option: ICountFilterOption = { generalMessage: true }) {
  return data.dayMessages.map((dayMessage) => {
    const count = filterMessage(dayMessage.messages, option).length
    return {
      day: dayMessage.dayText,
      count: count,
    }
  })
}

export function filterMessage(messages: Array<IMessage>, option: ICountFilterOption = { generalMessage: true }) {
  return messages.filter((message) => {
    return (
      (option.chartRoomSetting && message.messageType === eMessageType.ChatRoomSetting) ||
      (option.forceRemoveMember && message.messageType === eMessageType.ForceRemoveMember) ||
      (option.joinOrLeaveGroup && message.messageType === eMessageType.MemberJoinOrLeaveGroup) ||
      (option.autoReplyMessage && message.messageType === eMessageType.AutoReplyMessage) ||
      (option.systemForceRemoveMessage && message.messageType === eMessageType.SystemForceRemoveMessage) ||
      (option.revokeMessage && message.messageType === eMessageType.RevokeMessage) ||
      (option.stickerMessage && message.messageType === eMessageType.StickerMessage) ||
      (option.photoMessage && message.messageType === eMessageType.PhotoMessage) ||
      (option.videoMessage && message.messageType === eMessageType.VideoMessage) ||
      (option.generalMessage && message.messageType === eMessageType.GeneralMessage)
    )
  })
}

export function concatAllDaysMessages(daysMessages: Array<IDayMessages>) {
  return daysMessages.reduce((arr: Array<IMessage>, curr) => {
    arr.push(...curr.messages)
    return arr
  }, [])
}

export function concatAllMessagesToString(messages: Array<IMessage>) {
  return messages
    .reduce((arr: Array<string>, curr) => {
      arr.push(curr.message)
      return arr
    }, [])
    .join('\n')
}

// export function extractAllMessageByJieba(messageString: string, topk = 10) {
//   return jieba.extract(messageString, topk)
// }
