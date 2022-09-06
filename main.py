from dataset import *
from model import *

m = Model(path='models/test', n=4)
d = Dataset("data/kafka.txt")
m.train(d)
"""d = Dataset("data/cringe.txt")
m.train(d)
d = Dataset("data/toshnota.txt")
m.train(d)"""
for i in range(20):
    temp = m.generate()
    if len(temp.split()) > 4:
        print(temp)
