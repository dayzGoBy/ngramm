import numpy as np
import pandas as pd
from datetime import datetime
from functools import cmp_to_key
import os

def choice(d, base_frequency):
    segment = []
    if not d.keys():
        return ""
    for word in d.keys():
        segment.append([d[word], word])
    segment.sort(key=cmp_to_key(lambda x, y: 2*int(x[0] < y[0]) - 1))
    for i in range(1, len(segment)):
        segment[i][0] += segment[i-1][0]

    x = np.random.uniform(low=0, high=base_frequency)
    #do binary search instead
    res = ""
    for i in segment:
        if i[0] > x:
            res = i[1]
            break
    return res


class Model:
    n = 2
    data = pd.DataFrame()
    name = ""
    root_path = ""
    base_freq = {} # -> frequency
    next_freq = {} # -> pd.Series freq
    start_base = [] # -> is_start

    def __init__(self, k_gram=2, root_path="models/", name=str(datetime.now()), mode="create new model"):
        self.n = k_gram
        self.name = name
        self.root_path = root_path
        """if mode == "create new model":
            self.data = open(root_path+name, 'x')
            self.data = pd.DataFrame(columns=["phrase", "frequency", "next words", "is start"])
        elif mode == "upload model":
            self.data = pd.read_csv(root_path+name)"""

    def __phrase(self, sentence, x):
        phrase = ""
        for i in sentence[x: self.n - 1:]:
            phrase += (" " + i)
        return phrase

    def train(self, dataset):
        for sentence in dataset.get():
            # take first pair
            base = self.__phrase(sentence, 0)
            """if base not in self.data.index:
                self.data.append({'phrase': base, 'frequency': 0, 'next words': pd.Series(), 'is start': False})"""

            for i in range(0, len(sentence) - self.n + 1):
                base = self.__phrase(sentence, i)
                if i == 0:
                    self.start_base.append(base)
                    #state this base as starting one
                word = sentence[i+self.n-1]
                if base not in self.base_freq.keys():
                    self.base_freq[base] = 0
                self.base_freq[base] += 1
                if base not in self.next_freq.keys():
                    self.next_freq[base] = {}
                if word not in self.next_freq[base].keys():
                    self.next_freq[base][word] = 0
                self.next_freq[base][word] += 1
        print(self.next_freq)
        #self.data.to_csv(self.root_path+self.name)

    def generate(self, num_sentences, min_words):
        for s in range(num_sentences):
            temp = ""
            word = np.random.choice(self.start_base)
            temp += (word + " ")
            for w in range(min_words + np.random.randint(low=0, high=min_words)):
                if word == "":
                    word = np.random.choice(self.start_base)
                try:
                    word = choice(self.next_freq[word], self.base_freq[word])
                except KeyError:
                    print(self.next_freq[word])
                    print(self.base_freq[word])
                temp += (word + " ")

            temp = temp.strip()
            print(temp+".")

    def rename(self, name):
        os.rename(self.root_path + self.name, self.root_path + name)
        self.name = name
