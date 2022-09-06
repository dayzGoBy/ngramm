import re

# алфавит, используемый для генерации
a = re.compile(u'[а-яА-Я-]+|[.,:;?!]+')

# Класс датасета, является оберткой для массива текстовых единиц
class Dataset:
    units = []

    def __init__(self, path):
        # разбиваем текст на текстовые единицы
        for line in [line.lower() for line in open(path)]:
            for unit in a.findall(line):
                self.units.append(unit)

    def __str__(self):
        return str(self.units[1:11:])

    def get_units(self):
        return self.units

