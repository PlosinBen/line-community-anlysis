from pathlib import Path
from lib import Messages, Message, Rules, Rule
import re


def _init_rules() -> Rules:
    return Rules([
        Rule(  # 系統日期
            msg_group=Message.SYSTEM_GROUP,
            msg_type='date',
            regex=r'^(\d{2}\:\d{2})\t(.+)\t(.+)\n$'
        ),
        Rule(
            msg_group=Message.SYSTEM_GROUP,
            msg_type=Message.SYSTEM_ADMIN_OPERATE,
            regex=r'^(\d{2}\:\d{2})\t\t(.+)(已將聊天室的人數上限設為\d+人|變更了聊天室圖片|已將.+強制退出社群。)\n$'
        ),
        Rule(
            msg_group=Message.SYSTEM_GROUP,
            msg_type=Message.SYSTEM_AI_DELETE_MESSAGE,
            regex=r'^(\d{2}\:\d{2})\t\t(.+)(的訊息可能已違反社群服務條款而遭刪除)\n$'
        ),
        Rule(
            msg_group=Message.SYSTEM_GROUP,
            msg_type=Message.SYSTEM_USER_JOIN_LEAVE,
            regex=r'^(\d{2}\:\d{2})\t\t(.+)(加入聊天|離開聊天)\n$'
        ),
        Rule(
            msg_group=Message.USER_GROUP,
            msg_type=Message.USER_RETRACT,
            regex=r'^(\d{2}\:\d{2})\t\t(.+)(已收回訊息)\n$'
        ),
        Rule(
            msg_group=Message.USER_GROUP,
            msg_type=Message.USER_STICKER,
            regex=r'^(\d{2}\:\d{2})\t(.+)\t(\[貼圖\])\n$'
        ),
        Rule(
            msg_group=Message.USER_GROUP,
            msg_type=Message.USER_IMAGE,
            regex=r'^(\d{2}\:\d{2})\t(.+)\t(\[照片\])\n$'
        ),
        Rule(
            msg_group=Message.USER_GROUP,
            msg_type=Message.USER_TEXT,
            regex=r'^(\d{2}\:\d{2})\t(.+)\t(.+)\n$'
        ),
    ])


def get_file_version(filepath: Path) -> str:
    with filepath.open() as file_object:
        return '{}-{}'.format(
            re.match(f'^\[LINE\] (.+)的聊天', file_object.readline()).groups()[0],
            ''.join(re.findall(r'\d+', file_object.readline()))
        )


def parse_to_message(filepath: Path) -> Messages:
    with filepath.open() as file_object:
        messages = Messages(
            file_object.readline(),
            file_object.readline()
        )

        rules = _init_rules()

        file_object.readline()
        for line in file_object:
            # message date

            res = re.match(r'^(\d{4}\/\d{2}\/\d{2})（\w）\n$', line)
            if res is not None:
                message_date = res.groups()[0]
                continue

            match_rule = rules.match(line)
            if match_rule is not None:
                messages.push(
                    msg_group=match_rule.msg_group,
                    msg_type=match_rule.msg_type,
                    date=message_date,
                    *match_rule.match_groups
                )
            else:
                messages.compact(line)

    return messages
