import json
import os

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
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
async def get_info(image_name: str):
    file_path = os.path.join(TILES_DIR, image_name, f"info.json")
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Info not found")

    info = json.load(open(file_path, "r", encoding="utf8"))
    return JSONResponse(info)

@app.get("/api/info/{image_name}/preview.png")
async def get_preview(image_name: str):
    file_path = os.path.join(TILES_DIR, image_name, f"preview.png")
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Preview not found")

    return FileResponse(file_path)


class MarkerRequest(BaseModel):
    x: int
    y: int
    text: str


@app.post("/api/info/{image_name}/markers")
async def post_marker(image_name: str, data: MarkerRequest):
    file_path = os.path.join(TILES_DIR, image_name, f"info.json")
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Info not found")

    # Делаем на скорую руку, лучше базу данных.
    with open(file_path, "r", encoding="utf8") as jsonFile:
        info = json.load(jsonFile)

    info["markers"][len(info["markers"])+1] = {
        "x": data.x,
        "y": data.y,
        "text": data.text
    }

    with open(file_path, 'w', encoding="utf8") as f:
        json.dump(info, f, )
        print(f"Файл перезаписан: {info}")

    return JSONResponse(info)

@app.delete("/api/info/{image_name}/markers/{marker_id}")
async def delete_marker(image_name: str):
    file_path = os.path.join(TILES_DIR, image_name, f"info.json")
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Info not found")

    with open(file_path, "r", encoding="utf8") as jsonFile:
        info = json.load(jsonFile)

    del info["markers"]["marker_id"]

    with open(file_path, 'w') as f:
        json.dump(info, f)

    return JSONResponse(info)

@app.delete("/api/info/{image_name}/markers")
async def delete_markers(image_name: str):
    file_path = os.path.join(TILES_DIR, image_name, f"info.json")
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Info not found")

    with open(file_path, "r", encoding="utf8") as jsonFile:
        info = json.load(jsonFile)

    info["markers"] = {}

    with open(file_path, 'w', encoding="utf8") as f:
        json.dump(info, f)

    return JSONResponse(info)


@app.get("/api/tiles/{image_name}/{size}/{x}_{y}.png")
async def get_tile(image_name: str, size: int, x: int, y: int):
    file_path = os.path.join(TILES_DIR, image_name, f"level_{size}", f"{x}_{y}.png")
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Tile not found")

    return FileResponse(file_path)

# Команда для запуска сервера:
# uvicorn main:app --reload
