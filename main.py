from dataset import *
from model import *

d = Dataset("data/cringe.txt")
print(d)
m = Model()
m.train(d)
m.generate(11, 5)
