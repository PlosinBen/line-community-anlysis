import json

data = ""
with open("../.data/system_message.json") as fileobject:
    for line in fileobject:
        data += line

data = json.loads(data)

data = filter(
    lambda msg: msg['text'] == "的訊息可能已違反社群服務條款而遭刪除。",
    data
)

statistics_group = {}
for element in data:
    statistics = statistics_group.get(element['name'])
    if statistics is None:
        statistics = dict(
            name=element['name'],
            num=0
        )
        statistics_group[element['name']] = statistics
    statistics['num'] += 1

sorted_statistics = sorted(
    list(statistics_group.values()),
    key=lambda element: element['num'],
    reverse=True
)[:20]

print("遭AI次數 Top 20")
for element in sorted_statistics:
    print(element['name'], element['num'])

