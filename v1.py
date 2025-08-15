from fastapi import FastAPI, File, UploadFile, Form
from starlette.responses import PlainTextResponse
from supabase import create_client

from commons.constants import SUPABASE_URL, SUPABASE_KEY
from service.process_image_internal import get_dominant_color_name

# Sub-app for v1
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
app_v1 = FastAPI()


@app_v1.get('/',
            summary="Root endpoint",
            description="Returns a success message.",
            tags=["General"]
            )
async def home_root():
    return {'message': 'Success'}


@app_v1.post(
    '/process_image/',
    response_class=PlainTextResponse,
    summary="Process image to get a dominant color",
    description="Uploads an image and returns its dominant color name.",
    tags=["General"]
)
async def process_image(file: UploadFile = File(..., description="Image file to process")):
    return get_dominant_color_name(file.file)


@app_v1.post(
    '/upload',
    summary="Upload image to the bucket",
    description="Uploads an image to Supabase storage and returns its public URL.",
    tags=["Bucket"]
)
async def upload_image(file: UploadFile = File(..., description="Image file to upload")):
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


@app_v1.delete(
    '/delete',
    summary="Delete all images from the bucket",
    description="Deletes all images from Supabase storage.",
    tags=["Bucket"]
)
async def delete_all_images():
    files = supabase.storage.from_('images').list()
    names = [file.get('name') for file in files]
    supabase.storage.from_('images').remove(names)
    return {'message': 'All images deleted successfully from bucket'}


@app_v1.post(
    '/add',
    summary="Add clothing item",
    description="Adds a clothing item with filename and color to the database.",
    tags=["Clothes"]
)
async def add_clothing_item(
        filename: str = Form(..., description="Filename of the clothing item"),
        color: str = Form(..., description="Color of the clothing item")
):
    supabase.table("clothes").upsert({"filename": filename, "color": color}).execute()
    return {'message': f"Added file {filename} with color {color} to database"}


@app_v1.put(
    '/edit',
    summary="Edit clothing item color",
    description="Updates the color of a clothing item in the database.",
    tags=["Clothes"]
)
async def edit_clothing_item(filename: str = Form(...), new_color: str = Form(...)):
    supabase.table("clothes").update({"color": new_color}).eq("filename", filename).execute()
    return {'message': f"Updated file {filename} color to {new_color} in database"}


@app_v1.delete(
    '/delete/{filename}',
    summary="Delete clothing item",
    description="Deletes a clothing item and its image from storage.",
    tags=["Clothes"]
)
async def delete_clothing_item(filename: str):
    supabase.table("clothes").delete().eq("filename", filename).execute()
    supabase.storage.from_('images').remove([filename])
    return {'message': f'File {filename} deleted successfully'}


@app_v1.get(
    '/get_clothes',
    summary="Get all clothes",
    description="Returns a list of all clothing items with their filename and color.",
    tags=["Clothes"]
)
async def get_clothes():
    response = supabase.table("clothes").select("filename", "color").execute()
    return [(item['filename'], item['color']) for item in response.data][::-1]


@app_v1.get(
    '/get_color_names',
    summary="Get all color names",
    description="Returns a list of all color names from the database.",
    tags=["Colors"]
)
async def get_color_names():
    response = supabase.table("colors").select("color").execute()
    return [row["color"] for row in response.data]


@app_v1.post(
    '/get_combinations/',
    summary="Get color combinations by mode",
    description="Returns related colors for a given mode and color.",
    tags=["Combinations"]
)
async def get_combinations(mode: str = Form(...), color: str = Form(...)):
    response = supabase.table("combinations").select("related_color").eq("mode", mode).eq("color", color).execute()
    return [row["related_color"] for row in response.data]


@app_v1.post(
    '/get_ids',
    summary="Get clothes ids by color",
    description="Returns filenames of clothing items matching given colors, excluding a specific filename.",
    tags=["Clothes"]
)
async def get_ids(colors: list[str] = Form(...), exclude_id: str = Form(...)):
    response = supabase.table("clothes").select("filename").in_("color", colors).neq("filename", exclude_id).execute()
    return [row["filename"] for row in response.data]
