import os

from colorthief import ColorThief
from fastapi import FastAPI, File, UploadFile
from skimage.color import deltaE_ciede2000, rgb2lab

from colors import colors

app = FastAPI()


def closest_color_name(rgb):
    rgb1 = [x / 255 for x in rgb]
    min_colors = {}
    for color in colors:
        diff = deltaE_ciede2000(rgb2lab(rgb1), color.lab)
        min_colors[diff] = color.name
    return min_colors[min(min_colors.keys())]


def get_dominant_color_name(file):
    color_thief = ColorThief(file)
    dominant_color = color_thief.get_color()
    return closest_color_name(dominant_color)


@app.post("/do/")
async def do(file: UploadFile = File(...)):
    total_memory, used_memory, free_memory = map(
        int, os.popen('free -t -m').readlines()[-1].split()[1:])
    print("RAM memory % used:", round((used_memory / total_memory) * 100, 2))

    print(f'Get a file named {file.file.name} and size {file.size}')
    output = get_dominant_color_name(file.file)
    print('Background removed')
    return {"message": "Background removed", "filename": file.filename, "color": output}


@app.get("/")
async def home_root():
    return {"message": "Success"}
