import argparse
from model import *

parser = argparse.ArgumentParser(description='generate')
parser.add_argument('model', type=str, help='where the model is saved')
parser.add_argument('prefix', type=str, help='start of the sentence')
parser.add_argument('length', type=str, help='number of generated sentences')

args = parser.parse_args()

model = Model(path=args.model)

for i in range(args.length):
    print(model.generate(args.prefix))




