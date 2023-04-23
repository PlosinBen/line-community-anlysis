import sys
import re
import os
from lib.message import Messages
import getopt
# from word_cloud import WordCloudAction
#
# actions = dict(
#     report="report",
#     wordcloud=WordCloudAction
# )
#
#
# def usage():
#     print('''usage:
# main.py [action]
#
# actions:
# report: 內容分析
# wordcloud: 文字雲
# ''', end=''
#           )
#
#
# if __name__ == '__main__':
#     args = sys.argv[1:]
#
#     if len(args) == 0 or args[0] not in actions:
#         usage()
#         exit(0)
#
#     actions.get(args[0]).execute(args[1:])


def write_file(msg: Messages):
    with open(".data/messages/{}.json".format(msg.version), 'w') as file_object:
        file_object.write(str(msg))


if __name__ == '__main__':
    filename = 'record2-copy.txt'
    if len(sys.argv) > 1:
        filename = sys.argv[1]

    with open(filename) as fileobject:
        messages = Messages(
            fileobject.readline(),
            ''.join(re.findall(r'\d+', fileobject.readline()))
        )

        if os.path.isfile(".data/messages/{}.json".format(messages.version)):
            print("version exists")
            exit(0)

        # empty line
        fileobject.readline()
        for line in fileobject:
            # message date
            res = re.match(r'^(\d{4}\/\d{2}\/\d{2})（\w）\n$', line)
            if res is not None:
                message_date = res.groups()[0]
                continue

            res = re.match(
                r'^(\d{2}\:\d{2})\t\t(.+)(已將聊天室的人數上限設為\d+人|變更了聊天室圖片|已將.+強制退出社群。)\n$', line)
            if res is not None:
                messages.push('system_message', 'admin_operate', message_date, *res.groups())
                continue

            res = re.match(r'^(\d{2}\:\d{2})\t\t(.+)(的訊息可能已違反社群服務條款而遭刪除)\n$', line)
            if res is not None:
                messages.push('system_message', 'ai_delete_message', message_date, *res.groups())
                continue

            res = re.match(r'^(\d{2}\:\d{2})\t\t(.+)(加入聊天|離開聊天)\n$', line)
            if res is not None:
                messages.push('system_message', 'user_join_leave', message_date, *res.groups())
                continue

            res = re.match(r'^(\d{2}\:\d{2})\t\t(.+)(已收回訊息)\n$', line)
            if res is not None:
                messages.push('message', 'retract_message', message_date, *res.groups())
                continue

            res = re.match(r'^(\d{2}\:\d{2})\t(.+)\t([貼圖])\n$', line)
            if res is not None:
                messages.push('message', 'sticker', message_date, *res.groups())
                continue
            res = re.match(r'^(\d{2}\:\d{2})\t(.+)\t([照片])\n$', line)
            if res is not None:
                messages.push('message', 'image', message_date, *res.groups())
                continue

            res = re.match(r'^(\d{2}\:\d{2})\t(.+)\t(.+)\n$', line)
            if res is not None:
                messages.push('message', 'text', message_date, *res.groups())
                continue

            messages.compact(line)

    write_file(messages)
