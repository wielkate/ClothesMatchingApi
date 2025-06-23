import logging
import csv

from commons.constants import COLORS_CSV
from models.Color import Color

logger = logging.getLogger(__name__)


def load_colors():
    file = open(file=COLORS_CSV, mode='r', encoding='utf-8')
    return [
        Color(row[0], row[1], row[2], row[3])
        for row in csv.reader(file, delimiter=',')
    ]

global_colors = load_colors()