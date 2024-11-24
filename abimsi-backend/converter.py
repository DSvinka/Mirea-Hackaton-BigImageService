from concurrent.futures import ThreadPoolExecutor
from PIL import Image
import numpy as np
import os


Image.MAX_IMAGE_PIXELS = None

def process_tile(image_array, top, left, bottom, right, tile_row, tile_id, output_dir, levels: list[tuple[int, float]]):
    tile = image_array[top:bottom, left:right]
    tile_image = Image.fromarray(tile)
    for level, coeff in levels:
        level_folder = os.path.join(output_dir, f"level_{level}")
        try:
            if not os.path.exists(level_folder):
                os.mkdir(level_folder)
        except Exception as e:
            print(e)

        tile_filename = os.path.join(level_folder, f"{tile_row}_{tile_id}.png")

        if level != 0:
            size = tile_image.size
            tile_compressed = tile_image.resize((int(size[0] * coeff), int(size[1] * coeff)), Image.Resampling.LANCZOS)
            tile_compressed.save(tile_filename)
        else:
            tile_image.save(tile_filename)

        print(f"Сохранена плитка: {tile_filename} (Сжатие - {coeff} [{level}/{len(levels)}])")


def split_image_multithreaded(image_path, output_dir, tile_width, tile_height, levels: list[tuple[int, float]], max_threads=8):
    image = Image.open(image_path)
    image_array = np.array(image)

    img_height, img_width = image_array.shape[:2]

    os.makedirs(output_dir, exist_ok=True)

    tasks = []
    tile_id = 0
    tile_row = 0

    # Создание потоков
    with ThreadPoolExecutor(max_threads) as executor:
        for top in range(0, img_height, tile_height):
            for left in range(0, img_width, tile_width):
                bottom = min(top + tile_height, img_height)
                right = min(left + tile_width, img_width)
                tasks.append(
                    executor.submit(
                        process_tile,
                        image_array,
                        top,
                        left,
                        bottom,
                        right,
                        tile_row,
                        tile_id,
                        output_dir,
                        levels
                    )
                )
                tile_id += 2048
            tile_row += 2048
            tile_id = 0

        # Ожидаем завершения всех задач
        for task in tasks:
            task.result()


def create_preview(image, output_dir, preview_size=(512, 512)):
    """Создаёт превью изображения."""
    preview_path = os.path.join(output_dir, "preview.png")
    os.makedirs(output_dir, exist_ok=True)

    preview_image = image.resize(preview_size, Image.Resampling.LANCZOS)
    preview_image.save(preview_path)
    print(f"Сохранено превью: {preview_path}")

# Пример использования
split_image_multithreaded(
    image_path="image_1_level_0.png",  # Путь к большому изображению
    output_dir="tiles\\bio_cut",    # Папка для сохранения плиток
    tile_width=2048,               # Ширина плитки
    tile_height=2048,              # Высота плитки
    max_threads=12,                # Количество потоков
    levels=[
        (5, 0.1),
        (4, 0.15),
        (3, 0.20),
        (2, 0.25),
        (2, 0.45),
        (1, 0.5),
        (0, 0)
    ]
)

create_preview(Image.open("image_1_level_2.png"), output_dir="tiles\\bio_cut", preview_size=(512, 512))