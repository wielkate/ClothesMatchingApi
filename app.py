import logging
import os

from fastapi import FastAPI, File, UploadFile, Form
from supabase import create_client

from clothes import add, edit, delete, load_clothes
from commons.global_colors import load_colors
from commons.global_combinations import load_combinations
from service.process_image_internal import get_dominant_color_name

GREY_LIGHT = '\033[37m'
WHITE = '\033[97m'
GREEN = '\033[92m'
CYAN = '\033[36m'

logging.basicConfig(
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S',
    format=f'{CYAN}%(asctime)s  {GREY_LIGHT}%(name)s  {GREEN}[%(levelname)s]: {WHITE}%(message)s'
)
logger = logging.getLogger(__name__)

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
app = FastAPI()


@app.post('/process_image/')
async def process_image(file: UploadFile = File(...)):
    color = get_dominant_color_name(file.file)
    return {'message': 'Color name determined', 'filename': file.filename, 'color': color}


@app.get('/')
async def home_root():
    return {'message': 'Success'}


@app.post('/upload')
async def upload_image(file: UploadFile = File(...)):
    content = await file.read()
    supabase.storage.from_('images').upload(
        path=file.filename,
        file=content,
        file_options={
            'upsert': 'true',
            'content-type': file.content_type or 'image/png',
        },
    )
    url = supabase.storage.from_('images').get_public_url(file.filename)
    return {'url': url}


@app.delete('/delete')
async def delete_all_images():
    files = supabase.storage.from_('images').list()
    names = [file.get('name') for file in files]
    supabase.storage.from_('images').remove(names)
    return {'message': 'All images deleted successfully from bucket'}


@app.post('/add')
async def add_clothing_item(filename: str = Form(...), color: str = Form(...)):
    add(filename, color)
    return {'message': f"Added file {filename} with color {color} to database"}


@app.put('/edit')
async def edit_clothing_item(filename: str = Form(...), new_color: str = Form(...)):
    edit(filename, new_color)
    return {'message': f"Updated file {filename} color to {new_color} in database"}


@app.delete('/delete/{filename}')
async def delete_clothing_item(filename: str):
    delete(filename)
    supabase.storage.from_('images').remove([filename])
    return {'message': f'File {filename} deleted successfully'}


@app.get('/get_clothes', response_model=list[tuple[str, str]])
async def get_all_clothes():
    return load_clothes()


@app.get('/get_all_combinations/{mode}')
async def get_all_combinations(mode: str):
    return load_combinations(mode)


@app.get('/get_color_names')
async def get_color_names():
    return [color.name for color in load_colors()]
