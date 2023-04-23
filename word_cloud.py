from abc import ABC
from sys import argv
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
from tokenization_jieba import tokenization
from lib import Messages, download_resource, process_cache, Action


# def usage():
#     pass
#
#
# class WordCloudAction(Action, ABC):
#     @staticmethod
#     def usage():
#         print("Run word cloud")a
#         pass
#
#     @staticmethod
#     def execute(args: list[str]):
#         print("Run word cloud")
#         pass


# if __name__ == '__main__':
#
#     WordCloudAction.execute(argv[1:])


font_path = download_resource('https://github.com/tkiapril/source-fonts/raw/master/SourceHanSansTW-Regular.otf')

message = ''
with open('./.data/messages/202304211826.json') as file_object:
    for line in file_object:
        message += line

message = Messages.make(message)

targetMessages = filter(
    lambda message: message.is_text_message() and message.name == '探吉教-淡藍羽翼的韭韭TMF',
    message.data
)


@process_cache('tokenization', message.version)
def tokenization_message(msg: str):
    return tokenization(msg, 200)


tokenization_result = tokenization_message("\n".join([message.text for message in targetMessages]))

freq = tokenization_result.frequency()

stopwords = [
    'www',
    'https',
    'com',
    'tw',
    '比較',
    'emoji',
    'E6%',
    '--',
    '....',
    '...'
]

for stopword in stopwords:
    if freq.get(stopword) is not None:
        freq.pop(stopword)

wordcloud = WordCloud(
    font_path=font_path,
    width=4000,
    height=3000,
    margin=3,
    background_color="white",
    min_font_size=8,
).generate_from_frequencies(freq)

wordcloud.to_file("wordcloud.png")

plt.rcParams['font.sans-serif'] = ['Source Han Sans TW']
plt.figure(figsize=(4, 3.5), dpi=400)
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.title('探吉教-淡藍羽翼的韭韭TMF')
plt.show()

plt.savefig('my_plot.png')
