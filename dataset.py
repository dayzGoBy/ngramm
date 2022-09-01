import re

class Dataset:

    def __init__(self, path):
        file = open(path, 'r')
        #ПЕРВЫЙ ЭТАП
        re.split(r'(?<=[.!?…]) ', file.read())


    def shape(self):
        pass
