import random
import numpy as np
from collections import defaultdict
from random import uniform
from datetime import datetime
from functools import cmp_to_key

# статический метод для вероятностного выбора следующего после фразы слова
def choice(d):
    """
    :param d: хэшмап, в котором хранятся частоты каждого слова, следующего после определенной фразы фразы
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

    x = np.random.uniform(low=0, high=1)
    # do binary search instead
    res = ""
    for i in segment:
        if i[0] > x:
            res = i[1]
            break
    return res

def gen_n_grams(units, n=3):
    if n == 3:
        w0, w1 = 'blank', 'blank'
        for w2 in units:
            yield w0, w1, w2
            if w2 in '.!?':
                yield w1, w2, 'blank'
                yield w2, 'blank', 'blank'
                w0, w1 = 'blank', 'blank'
            else:
                w0, w1 = w1, w2
    elif n > 3:
        n_min_one = ['blank' for i in range(n - 1)]
        for w in units:
            yield *n_min_one, w
            if w in '.!?':
                yield *n_min_one[1::], 'blank'
                yield *n_min_one[2::], 'blank', 'blank'
                n_min_one = ['blank' for i in range(n - 1)]
            else:
                n_min_one = [i for i in list(n_min_one.append(w)[1::])]

    else:
        # выдавай исключение
        pass

# класс, объектом которого является модель
class Model:
    # по умолчанию используем биграмную модель
    n = 3
    # путь до папки, в которой лежит модель
    path = ""
    # частоты n - грамм
    n_seq = defaultdict(lambda: 0.0)
    # частоты n-1 - грамм
    base_seq = defaultdict(lambda: 0.0)
    # хэшмап, в которой каждой n-1 - грамме ставится в соответствие пара (слово, вероятность)
    model = {}
    is_normalized = False

    # инициализируем модель, создавая датафрейм для ее хранения или загружая его из csv
    def __init__(self, n=3, path="models/test", mode="create"):
        self.n = n
        self.path = path
        if mode == "create":
            # создаем файлы в которых будет храниться модель
            open(path+"/base.npy")
            open(path+"/n_seq.npy")

    # метод, обучающий модель на датасете
    def train(self, dataset):
        #TODO: реализуй общий случай
        n_grams = gen_n_grams(dataset.get_units(), n=self.n)
        self.is_normalized = False

        for w0, w1, w2 in n_grams:
            self.base_seq[w0, w1] += 1
            self.n_seq[w0, w1, w2] += 1

    # сохранение модели в два файла (временно, хочу потом в один)
        np.save(self.path+'/base.npy', dict(self.base_seq))
        np.save(self.path+'/n_seq.npy', dict(self.n_seq))

    # метод, генерирующий вероятности слов. Позволяет дообучать модель на другом датасете
    def __set_probabilities(self):
        self.model = {}
        self.is_normalized = True
        for (w0, w1, w2), freq in self.n_seq.items():
            if (w0, w1) in self.model:
                self.model[w0, w1].append((w2, freq / self.base_seq[w0, w1]))
            else:
                self.model[w0, w1] = [(w2, freq / self.base_seq[w0, w1])]

    # метод, отвечающий за генерацию отдельных предложений
    def generate(self):
        # проверяем, посчитаны ли вероятности
        if not self.is_normalized:
            self.__set_probabilities()
        phrase = ''
        t0, t1 = 'blank', 'blank'
        while 1:
            #TODO: сделай нормальный выбор следующего
            t0, t1 = t1, self.model[t0, t1][random.randint(0, len(self.model[t0, t1])-1)][0]
            if t1 == 'blank':
                break
            if t1 in ".!?,;:" or t0 == 'blank':
                phrase += t1
            else:
                phrase += ' ' + t1
        return phrase.capitalize()
