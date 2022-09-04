import numpy as np
import pandas as pd
from datetime import datetime
from functools import cmp_to_key
import os

# статический метод для вероятностного выбора следующего после фразы слова
def choice(d, base_frequency):
    """
    :param d: хэшмап, в котором хранятся частоты каждого слова, следующего после определенной фразы фразы
    :param base_frequency: частота фразы
    :return: следующее слово

    Суть метода заключается в том, что следующее слово выбирается с той же вероятностью, с какой она встречается в
    тексте после этой фразы. Он реализован следующим образом - сначала все слова сортируются по убыванию вероятности,
    затем отрезок [0, 1] разбивается на части, равные этим вероятностям (в том же порядке). Генерируется случайное
    число из [0, 1], и та часть отрезка, которой принадлежит это число, выбирается нами в качестве соответствующей
    искомому слову. Очевидно, вероятность "выпадения" этого слова будет той же, что и в тексте
    """
    segment = []
    if not d.keys():
        return ""
    for word in d.keys():
        segment.append([d[word], word])
    segment.sort(key=cmp_to_key(lambda x, y: 2 * int(x[0] < y[0]) - 1))
    for i in range(1, len(segment)):
        segment[i][0] += segment[i - 1][0]

    x = np.random.uniform(low=0, high=base_frequency)
    # do binary search instead
    res = ""
    for i in segment:
        if i[0] > x:
            res = i[1]
            break
    return res

# TODO: переписать все это на pandas
# класс, объектом которого является модель
class Model:
    # по умолчанию используем биграмную модель
    n = 2
    # датафрейм, в котором содержаться данные обучения модели
    data = pd.DataFrame()
    # имя модели (также имя csv-файла, в который она сохранится)
    name = ""
    # путь до папки, в которой лежит модель
    root_path = ""
    base_freq = {}  # -> frequency
    next_freq = {}  # -> pd.Series freq
    start_base = []  # -> is_start

    # инициализируем модель, создавая датафрейм для ее хранения или загружая его из csv
    def __init__(self, k_gram=2, root_path="models/", name=str(datetime.now()), mode="create new model"):
        self.n = k_gram
        self.name = name
        self.root_path = root_path
        """if mode == "create new model":
            self.data = open(root_path+name, 'x')
            self.data = pd.DataFrame(columns=["phrase", "frequency", "next words", "is start"])
        elif mode == "upload model":
            self.data = pd.read_csv(root_path+name)"""

    # приватный вспомогательный метод, который возвращает фразу длиной n-1 начиная с x-го слова из данного предложения
    def __phrase(self, sentence, x):
        phrase = ""
        for i in sentence[x: self.n - 1:]:
            phrase += (" " + i)
        return phrase

    # метод, обучающий модель на датасете
    def train(self, dataset):
        # будем обучать на отдельных предложениях, так как связи между концом одного предложения и началом другого нет
        for sentence in dataset.get():
            # base - это "базовая" фраза, слово за которой мы смотрим
            base = self.__phrase(sentence, 0)
            """if base not in self.data.index:
                self.data.append({'phrase': base, 'frequency': 0, 'next words': pd.Series(), 'is start': False})"""
            # пробегаем все базовые фразы в предложении
            for i in range(0, len(sentence) - self.n + 1):
                base = self.__phrase(sentence, i)
                if i == 0:
                    self.start_base.append(base)
                    # state this base as starting one
                word = sentence[i + self.n - 1]
                if base not in self.base_freq.keys():
                    self.base_freq[base] = 0
                self.base_freq[base] += 1
                if base not in self.next_freq.keys():
                    self.next_freq[base] = {}
                if word not in self.next_freq[base].keys():
                    self.next_freq[base][word] = 0
                self.next_freq[base][word] += 1
        print(self.next_freq)
        # self.data.to_csv(self.root_path+self.name)

    # метод, отвечающий за генерацию предложений
    def generate(self, num_sentences, min_words):
        # генерируем нужное количество предложений
        for s in range(num_sentences):
            temp = ""
            # случайно выбираем фразу, с которой начнется предложение
            word = np.random.choice(self.start_base)
            temp += (word + " ")
            for w in range(min_words + np.random.randint(low=0, high=min_words)):
                if word == "":
                    word = np.random.choice(self.start_base)
                try:
                    # вероятностно выбираем следующее слово
                    word = choice(self.next_freq[word], self.base_freq[word])
                except KeyError:
                    pass
                temp += (word + " ")

            temp = temp.strip()
            print(temp + ".")

    # метод, переименовывающий модель
    def rename(self, name):
        os.rename(self.root_path + self.name, self.root_path + name)
        self.name = name
