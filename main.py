from dataset import *
from model import *

d = Dataset("data/kafka.txt")
m = Model()
m.train(d)
m.generate(11, 5)
