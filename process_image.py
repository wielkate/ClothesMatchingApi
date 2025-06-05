from io import BytesIO

from PIL import Image  # can be cv2 or bytes
from colorthief import ColorThief
from rembg import remove
from skimage.color import rgb2lab, deltaE_ciede2000

from colors import colors


def closest_color_name(rgb):
    rgb1 = [x / 255 for x in rgb]
    min_colors = {}
    for color in colors:
        diff = deltaE_ciede2000(rgb2lab(rgb1), color.lab)
        min_colors[diff] = color.name
    return min_colors[min(min_colors.keys())]


def pil_to_bytes(image):
    image_bytes = BytesIO()
    image.save(image_bytes, format='PNG')
    image_bytes.seek(0)
    return image_bytes


def get_dominant_color_name(image):
    color_thief = ColorThief(pil_to_bytes(image))
    dominant_color = color_thief.get_color()
    return closest_color_name(dominant_color)


def remove_bg(file):
    image = Image.open(file)
    return remove(image)


def process_image_internal(file):
    image_without_bg = remove_bg(file)
    return get_dominant_color_name(image_without_bg)
