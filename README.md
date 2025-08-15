# Clothes Matcher – Backend

Clothes Matcher is an application designed to help color-blind individuals match clothing items based on color.
Visit [this repository](https://github.com/wielkate/ClothesMatching) to learn more.

This is a FastAPI-based backend service for the Clothes Matcher application.
The service processes uploaded clothing images, determines their dominant colors, and stores them securely
in [Supabase](https://supabase.com/) storage.
Then lists items matched by color in three modes:

- Monochrome
- Complementary
- Analogous

The application is deployed by [Render](https://render.com/), so it is available online.

## Features

- **Image Upload API** – store images in the Supabase bucket.
- **Dominant Color Detection** – analyze uploaded images to determine primary color.
- **API Versioning** – v1 endpoints for forward compatibility.
- **Integration with Frontend** – consumed by the Flet-based client.
- **Database tables creating** - creates tables, filling `Colors` and `Combinations`

## Endpoints

![Endpointa](docs/img.png)

## Tech Stack

- **Language:** Python 3.12+
- **Framework:** FastAPI
- **Storage and database:** Supabase (S3-compatible)
- **Deployment:** Render
- **Image Processing:** libraries `colorthief` and `skimage.color`
- **Color Database:** 140 colors supported by modern browsers

## Local usage

1. Clone this repository:
   ```bash
   git clone https://github.com/wielkate/ClothesMatchingApi.git
   cd ClothesMatchingApi

2. Ensure you are on master branch:
   ```bash
   git checkout master

3. Install all the necessary dependencies:
   ```bash
   pip install -r requirements.txt

4. Start the server:
   ```bash
   uvicorn app:app
   ```

> Configure environment variables `SUPABASE_URL` and `SUPABASE_KEY` in .env.

## Folder structure

   ```yaml
   ClothesMatchingApi/
   ├── app.py              # FastAPI entry point
   ├── v1.py               # Endpoints for v1
   ├── commons/            # Constants and shared logic
   ├── service/            # Image processing functions
   └── requirements.txt    # Dependencies
   ```

## License

This project is licensed under the MIT License.