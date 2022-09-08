import argparse
import os
from model import *

parser = argparse.ArgumentParser(description='train')
parser.add_argument('inputdir', type=str, help='texts to train the model')
parser.add_argument('model', type=str, help='directory to save the model')

args = parser.parse_args()

model = Model(path=args.model)

library = [f for f in os.listdir(args.inputdir) if os.path.isfile(os.path.join(args.model, f))]

for book in library:
    d = Dataset(args.inputdir + "/" + book)
    model.train(d)



