import re
from pathlib import Path

from .lib import Messages, Message, Rules, Rule


class FileHeaderNotMatch(Exception):
    pass


def _init_rules() -> Rules:
    return Rules([
        # Rule(  # 系統日期
        #     msg_group=Message.SYSTEM_GROUP,
        #     msg_type='date',
        #     regex=r'^(\d{4}\/\d{2}\/\d{2})（\w）\n$'
        # ),
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


def get_name_version(filepath: Path) -> tuple[str, str] | None:
    with filepath.open() as file_object:
        group_name_match = re.match(r'^\[LINE\] (.+)的聊天\n$', file_object.readline())
        save_date_match = re.match(r'^儲存日期\： (\d{4})\/(\d{2})\/(\d{2}) (\d{2})\:(\d{2})', file_object.readline())

        if group_name_match is None or save_date_match is None:
            raise FileHeaderNotMatch

        return group_name_match.groups()[0], ''.join(save_date_match.groups())


def parse_to_message(filepath: Path) -> Messages:
    title, version = get_name_version(filepath)

    with filepath.open() as file_object:
        messages = Messages(title, version)

        rules = _init_rules()

        for _ in range(3):
            next(file_object)

        for line in file_object:
            # message date

            res = re.match(r'^(\d{4}\/\d{2}\/\d{2})（\w）\n$', line)
            if res is not None:
                message_date = res.groups()[0]
                continue

            match_rule = rules.match(line)
            if match_rule is not None:
                messages.push(
                    match_rule.msg_group,
                    match_rule.msg_type,
                    message_date,
                    *match_rule.match_groups
                )
            else:
                messages.compact(line)

    return messages
