from colorsys import rgb_to_hsv

from skimage.color import rgb2lab


class Color:
    def __init__(self, row):
        self.name = row[0]
        self.r = int(row[1]) / 255
        self.g = int(row[2]) / 255
        self.b = int(row[3]) / 255
        self.lab = rgb2lab([self.r, self.g, self.b])