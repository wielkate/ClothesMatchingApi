from fastapi import FastAPI, File, UploadFile

from process_image_internal import get_dominant_color_name

app = FastAPI()


@app.post("/process_image/")
async def process_image(file: UploadFile = File(...)):
    output = get_dominant_color_name(file.file)
    return {"message": "Determined color name", "filename": file.filename, "color": output}


@app.get("/")
async def home_root():
    return {"message": "Success"}
