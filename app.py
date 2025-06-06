import os

from colorthief import ColorThief
from fastapi import FastAPI, File, UploadFile

app = FastAPI()


def get_dominant_color_name(file):
    color_thief = ColorThief(file)
    dominant_color = color_thief.get_color()
    return dominant_color


@app.post("/do/")
async def do(file: UploadFile = File(...)):
    total_memory, used_memory, free_memory = map(
        int, os.popen('free -t -m').readlines()[-1].split()[1:])
    print("RAM memory % used:", round((used_memory / total_memory) * 100, 2))

    print(f'Get a file named {file.filename} and size {file.size}')
    output = get_dominant_color_name(file.file)
    print('Background removed')
    return {"message": "Background removed", "filename": file.filename, "color": output}


@app.get("/")
async def home_root():
    return {"message": "Success"}
