from model import *

""" Продемонстрируем генерацию текста моделью, обученной на двух первых томах 
"Войны и мира", "Волшебной горе" Томаса Манна, 
полном собрании сочинений Кафки и "Тошноте" Сартра"""

m = Model(path="models/four in a row")

for i in range(20):
    x = m.generate()
    if x is None:
        break
    print(x+"\n")

