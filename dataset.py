import re
import pandas as pd

# TODO: написать нормальную генерацию датасета и текста!!! и все
def to_words(s):
    res = ""
    temp = ""
    letters = "абвгдеёжзийклмнопрстуфхцчшщьыъэюя"
    for i in s.lower():
        if i in letters:
            temp += i
        else:
            res += (temp+" ")
            temp = ""

    return res.lstrip(" ").split()


class Dataset:
    sentences = []

    def __init__(self, path):
        file = open(path, 'r')
        # разбиваем текст на предложения
        split_regex = re.compile(r'[.|!|?|…]')
        self.sentences = [to_words(x) for x in filter(lambda t: t, [t.strip() for t in split_regex.split(file.read())])]

    def __str__(self):
        return str(self.sentences[1:5:])

    def get(self, min_sentence_size=3):
        return [x for x in self.sentences if len(x) >= min_sentence_size]

