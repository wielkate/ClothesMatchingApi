from fastapi import FastAPI, File, UploadFile
from rembg import remove

app = FastAPI()


@app.post("/remove_bg/")
async def remove_bg(file: UploadFile = File(...)):
    output = remove(file.file.read())
    return {"message": "Background removed", "filename": file.filename, "file": output}


@app.get("/")
async def home_root():
    return {"message": "Success"}
