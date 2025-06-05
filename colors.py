import csv

from Color import Color

COLORS_CSV = 'Colors.csv'


def __get_colors_from_csv__():
    file = open(file=COLORS_CSV, mode='r', encoding='utf-8')
    return [
        Color(row) for row in csv.reader(file, delimiter=',')
    ]


colors = __get_colors_from_csv__()
