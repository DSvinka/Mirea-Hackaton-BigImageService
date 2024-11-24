import json
import os

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse, JSONResponse

from config import TILES_DIR

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8080",
    "http://localhost:63343",
    "https://mirea.dsivnka.ru"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api")
def read_root():
    return {"message": "Tile server is running"}


@app.get("/api/info/{image_name}")
async def get_tile(image_name: str):
    file_path = os.path.join(TILES_DIR, image_name, f"info.json")
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Info not found")

    info = json.load(open(file_path, "rb"))
    return JSONResponse(info)

@app.get("/api/info/{image_name}/preview.png")
async def get_tile(image_name: str):
    file_path = os.path.join(TILES_DIR, image_name, f"preview.png")
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Preview not found")

    return FileResponse(file_path)

@app.get("/api/tiles/{image_name}/{size}/{x}_{y}.png")
async def get_tile(image_name: str, size: int, x: int, y: int):
    file_path = os.path.join(TILES_DIR, image_name, f"level_{size}", f"{x}_{y}.png")
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Tile not found")

    return FileResponse(file_path)

# Команда для запуска сервера:
# uvicorn main:app --reload
