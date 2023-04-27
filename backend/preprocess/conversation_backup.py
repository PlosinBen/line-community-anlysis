from backend.lib import Messages, Message, process_cache
from pathlib import Path
import re


def load_file_version(filepath: Path) -> str:
    with filepath.open() as file_object:
        return '{}-{}'.format(
            re.match(f'^\[LINE\] (.+)的聊天', file_object.readline()).groups()[0],
            ''.join(re.findall(r'\d+', file_object.readline()))
        )


def parse_file_content(filepath: Path) -> Messages:
    with filepath.open() as file_object:
        messages = Messages(
            file_object.readline(),
            file_object.readline()
        )

        file_object.readline()
        for line in file_object:
            # message date
            res = re.match(r'^(\d{4}\/\d{2}\/\d{2})（\w）\n$', line)
            if res is not None:
                message_date = res.groups()[0]
                continue

            res = re.match(
                r'^(\d{2}\:\d{2})\t\t(.+)(已將聊天室的人數上限設為\d+人|變更了聊天室圖片|已將.+強制退出社群。)\n$', line)
            if res is not None:
                messages.push(Message.SYSTEM_GROUP, Message.SYSTEM_ADMIN_OPERATE, message_date, *res.groups())
                continue

            res = re.match(r'^(\d{2}\:\d{2})\t\t(.+)(的訊息可能已違反社群服務條款而遭刪除)\n$', line)
            if res is not None:
                messages.push(Message.SYSTEM_GROUP, Message.SYSTEM_AI_DELETE_MESSAGE, message_date, *res.groups())
                continue

            res = re.match(r'^(\d{2}\:\d{2})\t\t(.+)(加入聊天|離開聊天)\n$', line)
            if res is not None:
                messages.push(Message.SYSTEM_GROUP, Message.SYSTEM_USER_JOIN_LEAVE, message_date, *res.groups())
                continue

            res = re.match(r'^(\d{2}\:\d{2})\t\t(.+)(已收回訊息)\n$', line)
            if res is not None:
                messages.push(Message.USER_GROUP, Message.USER_RETRACT, message_date, *res.groups())
                continue

            res = re.match(r'^(\d{2}\:\d{2})\t(.+)\t(\[貼圖\])\n$', line)
            if res is not None:
                messages.push(Message.USER_GROUP, Message.USER_STICKER, message_date, *res.groups())
                continue
            res = re.match(r'^(\d{2}\:\d{2})\t(.+)\t(\[照片\])\n$', line)
            if res is not None:
                messages.push(Message.USER_GROUP, Message.USER_IMAGE, message_date, *res.groups())
                continue

            res = re.match(r'^(\d{2}\:\d{2})\t(.+)\t(.+)\n$', line)
            if res is not None:
                messages.push(Message.USER_GROUP, Message.USER_TEXT, message_date, *res.groups())
                continue

            messages.compact(line)

    return messages


def preprocess(filepath: Path) -> Messages:
    file_version = load_file_version(filepath)

    @process_cache('message', file_version)
    def call_parse_file(target_file: Path) -> Messages:
        return parse_file_content(target_file)

    return call_parse_file(filepath)
