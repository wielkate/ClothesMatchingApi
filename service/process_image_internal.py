from colorthief import ColorThief
from skimage.color import deltaE_ciede2000, rgb2lab

from commons.global_colors import global_colors


def closest_color_name(rgb):
    rgb1 = [x / 255 for x in rgb]
    min_colors = {}
    for color in global_colors:
        diff = deltaE_ciede2000(rgb2lab(rgb1), color.lab)
        min_colors[diff] = color.name
    return min_colors[min(min_colors.keys())]


def get_dominant_color_name(file):
    color_thief = ColorThief(file)
    dominant_color = color_thief.get_color()
    return closest_color_name(dominant_color)
