from fastapi import UploadFile
from rembg import remove


def remove_bg(file: UploadFile):
    return remove(file.file.read())
