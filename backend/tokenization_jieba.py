import jieba
import jieba.analyse
from collections import Counter
from backend.lib import download_resource


class TokenizationResult:
    def __init__(self, tags: list[str], segments: list[str]):
        self.tags: list[str] = tags
        self.segments: list[str] = segments

    def frequency(self) -> dict[str, int]:
        freq = {}
        dictionary = Counter(self.segments)
        for ele in dictionary:
            if ele in self.tags:
                freq[ele] = dictionary[ele]
        return freq


def tokenization(content: str, tag_num: int = 200) -> TokenizationResult:
    dict_file_path = download_resource('https://raw.githubusercontent.com/ldkrsi/jieba-zh_TW/master/jieba/dict.txt')

    stop_words_file_path = download_resource('https://github.com/kdchang/python-jieba-chart/blob/master/stopwords.txt')

    jieba.set_dictionary(dict_file_path)
    jieba.analyse.set_stop_words(stop_words_file_path)

    tags = jieba.analyse.extract_tags(content, topK=tag_num)

    seg_list = jieba.lcut(content, cut_all=False)

    return TokenizationResult(tags, seg_list)
