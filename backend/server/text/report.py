from pathlib import Path
from backend.preprocess.conversation_backup import preprocess
from sys import argv
from backend.lib import Message
from datetime import datetime, timedelta


class StatisticsElement:
    def __init__(self, key):
        self.key: str = key
        self.num: int = 0

    def increase(self):
        self.num += 1


class StatisticsGroup:
    def __init__(self):
        self.elements: dict[str, StatisticsElement] = dict()

    def get(self, key: str):
        return self.elements.get(key).num if key in self.elements else 0

    def increase(self, key: str):
        if self.elements.get(key) is None:
            self.elements[key] = StatisticsElement(key)

        self.elements.get(key).increase()

    def get_top(self, num: int) -> list[StatisticsElement]:
        return sorted(
            list(self.elements.values()),
            key=lambda element: element.num,
            reverse=True
        )[:num]


class Statistics:
    def __init__(self):
        self.total_message = 0
        self.user_message = 0
        self.sys_message = 0

        self.user_statistics: StatisticsGroup = StatisticsGroup()
        self.user_sticker_statistics: StatisticsGroup = StatisticsGroup()
        self.date_statistics: StatisticsGroup = StatisticsGroup()
        self.date_user_statistics: dict[str, StatisticsGroup] = {}

    def increase_dialogue(self, message: Message):
        self.total_message += 1
        if message.is_sys_message():
            self.sys_message += 1
        else:
            self.user_message += 1

        self.date_statistics.increase(message.date)
        self.user_statistics.increase(message.name)

        if msg.is_sticker_message():
            self.user_sticker_statistics.increase(message.name)

        if self.date_user_statistics.get(message.date) is None:
            self.date_user_statistics[message.date] = StatisticsGroup()

        self.date_user_statistics.get(message.date).increase(message.name)

    def print_result(self):
        print("總訊息數: {:,}\t 發言使用者: {:,}\t 使用者訊息數: {:,}\t 發言使用者平均訊息數: {:,.1f}".format(
            self.total_message,
            len(self.date_user_statistics),
            self.user_message,
            self.user_message / len(self.date_user_statistics)
        ))

        print("訊息總數排名: ")
        for element in self.user_statistics.get_top(5):
            print('{} ({:,})'.format(element.key, element.num), end="\t")

        print("\n貼圖使用數排名: ")
        for element in self.user_sticker_statistics.get_top(5):
            print('{} ({:,})'.format(element.key, element.num), end="\t")

        print("\n每日訊息排名")
        for element in self.date_statistics.get_top(10):
            print(element.key, element.num, '\t', end="")
            for sub_element in self.date_user_statistics.get(element.key).get_top(5):
                print("{}({:,}) \t".format(sub_element.key, sub_element.num), end="")
            print("")

        print("近30日訊息數")
        today = datetime.today()
        for i in range(30, 0, -1):
            date = (today - timedelta(days=i)).strftime('%Y/%m/%d')
            print('{} {:,}'.format(
                date,
                self.date_statistics.get(date)
            ), end="\t")
            if i % 10 == 1:
                print()


filepath = Path(argv[1])

output = {
    'total_message'
}

if not filepath.is_file():
    print("file {} not exists".format(argv[1]))
    exit(0)

messages = preprocess(filepath)

message_count = len(messages.data)
user_message_count = len(messages.data)
messages = messages.filter(lambda msg: msg.is_user_message())

statistics = Statistics()
for msg in messages.data:
    statistics.increase_dialogue(msg)

print()
print(messages.title.strip())
print(messages.version.strip())

statistics.print_result()
