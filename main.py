from model import *

m = Model(path='models/faust')
for i in range(20):
    temp = m.generate()
    if len(temp.split()) > 1:
        print(temp)
