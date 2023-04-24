import json


class Message:
    SYSTEM_GROUP = 'system'
    USER_GROUP = 'user'

    SYSTEM_ADMIN_OPERATE = 'admin_operate'
    SYSTEM_AI_DELETE_MESSAGE = 'ai_delete_message'
    SYSTEM_USER_JOIN_LEAVE = 'user_join_leave'

    USER_RETRACT = 'retract'
    USER_STICKER = 'sticker'
    USER_IMAGE = 'image'
    USER_TEXT = 'text'

    def __init__(self, msg_group: str, msg_type: str, date: str, time: str, name: str, text: str = ''):
        self.msg_group: str = msg_group
        self.msg_type: str = msg_type
        self.date: str = date
        self.time: str = time
        self.name: str = name
        self.text: str = text

    def push(self, text: str):
        self.text += text
        return self

    def is_sys_message(self) -> bool:
        return self.msg_group == self.SYSTEM_GROUP

    def is_user_message(self) -> bool:
        return self.msg_group == self.USER_GROUP

    def is_retract_message(self):
        return self.msg_type == self.USER_RETRACT

    def is_image_message(self):
        return self.msg_type == self.USER_IMAGE

    def is_sticker_message(self):
        return self.msg_type == self.USER_STICKER

    def is_text_message(self):
        return self.msg_type == self.USER_TEXT

    def __str__(self):
        return json.dumps(self.__dict__, ensure_ascii=False)


class Messages:
    def __init__(self, title: str, version: str, data: list[Message] = None):
        self.title: str = title
        self.version = version
        self.data: list[Message] = [] if data is None or len(data) == 0 else data

    def push(self, msg_group: str, msg_type: str, date: str, time: str, name: str, text: str):
        self.data.append(Message(msg_group, msg_type, date, time, name, text))

    def compact(self, text: str):
        self.data[-1].push(text)

    @staticmethod
    def make(content: str):
        content = json.loads(content)
        content['data'] = [Message(**el) for el in content['data']]

        return Messages(**content)

    def __str__(self):
        return json.dumps(
            dict(
                title=self.title,
                version=self.version,
                data=[msg.__dict__ for msg in self.data],
            )
            , ensure_ascii=False
        )
