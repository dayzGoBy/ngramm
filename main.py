from model import *

m = Model(path='models/faust', mode='load')
d = Dataset("data/faust.txt")
m.train(d)
"""d = Dataset("data/kafka.txt")
m.train(d)
d = Dataset("data/cringe.txt")
m.train(d)
d = Dataset("data/toshnota.txt")
m.train(d)"""
for i in range(20):
    temp = m.generate()
    if len(temp.split()) > 1:
        print(temp)
