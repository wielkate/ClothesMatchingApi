from colorsys import rgb_to_hsv

from skimage.color import rgb2lab


class Color:
    def __init__(self, name, r, g, b):
        self.name = name
        self.r = int(r) / 255
        self.g = int(g) / 255
        self.b = int(b) / 255
        self.lab = rgb2lab([self.r, self.g, self.b])
        self.hsv = self.__get_hsv_in_degrees_and_percentage__()

    def __get_hsv_in_degrees_and_percentage__(self):
        h, s, v = rgb_to_hsv(self.r, self.g, self.b)
        return h * 360, s * 100, v * 100
