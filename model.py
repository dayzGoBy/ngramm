import pickle
import random
import re
import os
import numpy as np
from collections import defaultdict
from functools import cmp_to_key

a = re.compile(u'[а-яА-Я-]+|[.,:;?!]+')  # алфавит

def choice(ver):  # статический метод для вероятностного выбора следующего после фразы слова
    """
    Суть метода заключается в том, что следующее слово выбирается с той же вероятностью, с какой она встречается в
    тексте после этой фразы. Он реализован следующим образом - сначала все слова сортируются по убыванию вероятности,
    затем отрезок [0, 1] разбивается на части, равные этим вероятностям (в том же порядке). Генерируется случайное
    число из [0, 1], и та часть отрезка, которой принадлежит это число, выбирается нами в качестве соответствующей
    искомому слову. Очевидно, вероятность "выпадения" этого слова будет той же, что и в тексте
    """
    ver.sort(key=cmp_to_key(lambda x1, x2: 2 * int(x1[1] < x2[1]) - 1))
    for i in range(1, len(ver)):
        ver[i][1] += ver[i - 1][1]

    x = np.random.uniform(low=0, high=1)
    # do binary search instead
    res = ver[0][0]
    for i in ver:
        if i[1] > x:
            res = i[0]
            break
    return res


class Model:  # класс, объектом которого является модель
    n = 3  # по умолчанию используем триграмную модель
    path = ""  # путь до папки, в которой лежит модель
    n_seq = defaultdict()  # частоты n - грамм
    base_seq = defaultdict()  # частоты n-1 - грамм
    model = {}  # хэшмап, в которой каждой n-1 - грамме ставится в соответствие пара (слово, вероятность)
    is_normalized = False

    def __init__(self, path="models/test", mode="load"):
        self.path = path
        if not os.path.exists(path + "/base.pkl") or not os.path.exists(path + "/n_seq.pkl"):
            mode = 'create'
        if mode == "create":  # создаем файлы в которых будет храниться модель
            open(path + "/base.pkl", "x")
            open(path + "/n_seq.pkl", "x")
        elif mode == "load":  # иначе загружаем данные из файлов
            self.base_seq = pickle.load(open(path + '/base.pkl', 'rb'))
            self.n_seq = pickle.load(open(path + '/n_seq.pkl', 'rb'))

    def gen_n_grams(self, units):
        w0, w1 = 'blank', 'blank'  # в самом начале присвоим двум словам фиктивные значения
        # это позволит не выделять отдельно начала предложений и детектировать их концы
        for w2 in units:
            yield w0, w1, w2
            if w2 in '.!?':  # встречен конец предложения, генератор возвращает две тройки, соответствующие
                # предпоследней и последней перед этим грамме
                yield w1, w2, 'blank'
                yield w2, 'blank', 'blank'
                w0, w1 = 'blank', 'blank'
            else:
                w0, w1 = w1, w2

    def train(self, dataset):  # метод, обучающий модель на датасете
        n_grams = self.gen_n_grams(dataset.get_units())  # генератор, возвращающий все n-граммы
        for w0, w1, w2 in n_grams:  # для каждой встреченной граммы увеличивается ее частота
            self.base_seq[w0, w1] += 1
            self.n_seq[w0, w1, w2] += 1

        self.is_normalized = False
        # сохранение модели в два файла
        pickle.dump(dict(self.base_seq), open(self.path + '/base.pkl', 'wb'))
        pickle.dump(dict(self.n_seq), open(self.path + '/n_seq.pkl', 'wb'))

    def __set_probabilities(self):  # метод, генерирующий вероятности слов
        # позволяет дообучать модель на другом датасете
        self.model = {}
        self.is_normalized = True
        for (w0, w1, w2), freq in self.n_seq.items():
            if (w0, w1) in self.model:
                self.model[w0, w1].append([w2, freq / self.base_seq[w0, w1]])
            else:
                self.model[w0, w1] = [[w2, freq / self.base_seq[w0, w1]]]

    def generate(self, prefix=""):  # метод, отвечающий за генерацию отдельных предложений
        if not self.is_normalized:  # проверяем, посчитаны ли вероятности
            self.__set_probabilities()
        phrase = ''
        w0, w1, w2 = 'blank', 'blank', 'blank'
        while 1:
            if (w0, w1) == ('blank', 'blank'):
                w0 = w1
                if prefix == "":
                    w1 = self.model[w0, w1][random.randint(0, len(self.model[w0, w1]) - 1)][0]
                else:
                    words = []
                    for unit in a.findall(prefix):
                        words.append(unit)

                    for i in words[:len(words) - 2:]:
                        phrase += (" " + i)

                    w0, w1 = words[len(words) - 2], words[len(words) - 1]

            else:
                w0, w1 = w1, choice(self.model[w0, w1])

            if w1 == 'blank':
                break
            if w1 in ".!?,;:" or w0 == 'blank':
                phrase += w1
            else:
                phrase += ' ' + w1
        return phrase.capitalize()


class Dataset:  # Класс датасета, является оберткой для массива текстовых единиц
    units = []

    def __init__(self, path):
        for line in [line.lower() for line in open(path)]:  # разбиваем текст на текстовые единицы
            for unit in a.findall(line):
                self.units.append(unit)

    def __str__(self):
        return str(self.units[1:11:])

    def get_units(self):
        return self.units