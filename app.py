import logging

from fastapi import FastAPI, File, UploadFile, Form
from starlette.responses import PlainTextResponse
from supabase import create_client

from commons.constants import SUPABASE_URL, SUPABASE_KEY
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

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
app = FastAPI()


@app.get('/')
async def home_root():
    return {'message': 'Success'}


@app.post('/process_image/', response_class=PlainTextResponse)
async def process_image(file: UploadFile = File(...)):
    return get_dominant_color_name(file.file)


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
    supabase.table("clothes").upsert({"filename": filename, "color": color}).execute()
    return {'message': f"Added file {filename} with color {color} to database"}


@app.put('/edit')
async def edit_clothing_item(filename: str = Form(...), new_color: str = Form(...)):
    supabase.table("clothes").update({"color": new_color}).eq("filename", filename).execute()
    return {'message': f"Updated file {filename} color to {new_color} in database"}


@app.delete('/delete/{filename}')
async def delete_clothing_item(filename: str):
    supabase.table("clothes").delete().eq("filename", filename).execute()
    supabase.storage.from_('images').remove([filename])
    return {'message': f'File {filename} deleted successfully'}


@app.get('/get_clothes')
async def get_clothes():
    response = supabase.table("clothes").select("filename", "color").execute()
    return [(item['filename'], item['color']) for item in response.data][::-1]


@app.get('/get_color_names')
async def get_color_names():
    response = supabase.table("colors").select("color").execute()
    return [row["color"] for row in response.data]


@app.post('/get_combinations/')
async def get_combinations(mode: str = Form(...), color: str = Form(...)):
    response = supabase.table("combinations").select("related_color").eq("mode", mode).eq("color", color).execute()
    return [row["related_color"] for row in response.data]


@app.post('/get_ids')
async def get_ids(colors: list[str] = Form(...), exclude_id: str = Form(...)):
    response = supabase.table("clothes").select("filename").in_("color", colors).neq("filename", exclude_id).execute()
    return [row["filename"] for row in response.data]
