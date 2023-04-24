from pathlib import Path
from preprocess.conversation_backup import preprocess
from sys import argv
import plotext as plt
import numpy as np
from datetime import datetime

filepath = Path(argv[1])

if not filepath.is_file():
    print("file {} not exists".format(argv[1]))
    exit(0)

time_message_count = np.zeros(24)

messages = preprocess(filepath)

# datetime.strptime(datetime_str, '%m/%d/%y')
today = datetime.today()
dates = {}
for message in messages.data:
    if message.is_sys_message():
        continue

    msg_date = datetime.strptime(message.date, '%Y/%m/%d')

    weekday = int(msg_date.strftime('%w'))

    if weekday == 0 or weekday > 5:
        continue

    delta = today - msg_date
    if delta.days > 32:
        continue

    if message.date not in dates:
        dates[message.date] = 0

    dates[message.date] += 1
    time_message_count[int(message.time.split(':')[0])] += 1

plt.simple_bar(
    np.floor(time_message_count * 100 / len(dates)) / 100
)

plt.title("群組訊息時間")
plt.show()

print(len(dates), dates)
