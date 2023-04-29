export interface IMessage {
  timestamp: number
  timeText: string
  member: string
  messageType: eMessageType
  message: string
}

export interface IDayMessages {
  timestamp: number
  dayText: string
  messages: Array<IMessage>
}

export interface IParseMessageResult {
  title: string
  storeAt: string
  userSets: Set<string>
  dayMessages: Array<IDayMessages>
}

export interface ICountFilterOption {
  [key: string]: boolean
  chartRoomSetting?: boolean
  forceRemoveMember?: boolean
  joinOrLeaveGroup?: boolean
  autoReplyMessage?: boolean
  systemForceRemoveMessage?: boolean
  revokeMessage?: boolean
  stickerMessage?: boolean
  photoMessage?: boolean
  videoMessage?: boolean
  generalMessage?: boolean
}
