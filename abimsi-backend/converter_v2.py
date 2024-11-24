from concurrent.futures import ProcessPoolExecutor
from PIL import Image
import os

Image.MAX_IMAGE_PIXELS = None

def process_row(image_path, top, bottom, tile_width, tile_height, output_dir, levels):
    image = Image.open(image_path)
    for left in range(0, image.width, tile_width):
        right = min(left + tile_width, image.width)
        tile = image.crop((left, top, right, bottom))
        for level, coeff in levels:
            level_folder = os.path.join(output_dir, f"level_{level}")
            os.makedirs(level_folder, exist_ok=True)
            tile_filename = os.path.join(level_folder, f"{top}_{left}.png")
            if level != 0:
                resized_tile = tile.resize((int(tile.width * coeff), int(tile.height * coeff)), Image.Resampling.LANCZOS)
                resized_tile.save(tile_filename)
            else:
                tile.save(tile_filename)

            print(f"Сохранена плитка: {tile_filename} (Сжатие - {coeff} [{level}/{len(levels)}])")

def split_image(image_path, output_dir, tile_width, tile_height, levels, max_threads=8):
    image = Image.open(image_path)
    os.makedirs(output_dir, exist_ok=True)

    with ProcessPoolExecutor(max_threads) as executor:
        for top in range(0, image.height, tile_height):
            bottom = min(top + tile_height, image.height)
            executor.submit(process_row, image_path, top, bottom, tile_width, tile_height, output_dir, levels)

if __name__ == "__main__":
    split_image(
        image_path="image_1_level_0.png",  # Путь к большому изображению
        output_dir="tiles\\microscope",    # Папка для сохранения плиток
        tile_width=2048,               # Ширина плитки
        tile_height=2048,              # Высота плитки
        max_threads=12,                # Количество потоков
        levels=[
            (5, 0.25),
            (4, 0.45),
            (3, 0.5),
            (2, 0.75),
            (1, 0.85),
            (0, 0)
        ]
    )