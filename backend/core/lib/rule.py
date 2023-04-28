# import re
#
#
# class Rule:
#     def __init__(self, msg_group: str, msg_type: str, regex: str, args_name: list[str] = ('time', 'name', 'text')):
#         self.msg_group: str = msg_group
#         self.msg_type: str = msg_type
#         self.regex: str = regex
#         self.args_name: list[str] = args_name
#
#
# class MatchRule:
#     def __init__(self):
#
# class Rules:
#     def __init__(self, rules: list[Rule] = ()):
#         self.rules: list[Rule] = rules
#
#     def match(self, msg: str):
#         for rule in self.rules:
#             result = re.match(rule.regex, msg)
#             if result is not None:
#                 return result
#
#     @staticmethod
#     def make():
#         return Rules([
#             Rule(
#                 'system_message',
#                 'admin_operate',
#                 r'^(\d{2}\:\d{2})\t\t(.+)(已將聊天室的人數上限設為\d+人|變更了聊天室圖片|已將.+強制退出社群。)\n$'
#             ),
#             Rule(
#                 'system_message',
#                 'ai_delete_message',
#                 r'^(\d{2}\:\d{2})\t\t(.+)(的訊息可能已違反社群服務條款而遭刪除。)\n$'
#             ),
#             Rule(
#                 'system_message',
#                 'user_join_leave',
#                 r'^(\d{2}\:\d{2})\t\t(.+)(加入聊天|離開聊天)\n$'
#             ),
#             Rule(
#                 'message',
#                 'retract_message',
#                 r'^(\d{2}\:\d{2})\t\t(.+)(已收回訊息)\n$'
#             ),
#             Rule(
#                 'message',
#                 'sticker',
#                 r'^(\d{2}\:\d{2})\t\t(.+)([貼圖])\n$'
#             ),
#             Rule(
#                 'message',
#                 'image',
#                 r'^(\d{2}\:\d{2})\t\t(.+)([照片])\n$'
#             ),
#             Rule(
#                 'message',
#                 'image',
#                 r'^(\d{2}\:\d{2})\t(.+)\t(.+)\n$'
#             ),
#         ])