import json


class Message:
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
        return self.msg_group == 'system_message'

    def is_message(self) -> bool:
        return self.msg_group == 'message'

    def is_text_message(self):
        return self.msg_type == 'text'

    def __str__(self):
        return json.dumps(self.__dict__, ensure_ascii=False)


class Messages:
    def __init__(self, title: str, version: str, data: list[Message] = ()):
        self.title: str = title
        self.version = version
        self.data: list[Message] = data

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
