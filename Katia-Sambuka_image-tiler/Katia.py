from concurrent.futures import ThreadPoolExecutor
from PIL import Image
import numpy as np
import os

Image.MAX_IMAGE_PIXELS = None

def process_tile(image_array, top, left, bottom, right, tile_row, tile_id, output_dir):
    tile = image_array[top:bottom, left:right]
    tile_image = Image.fromarray(tile)
    tile_filename = os.path.join(output_dir, f"{tile_row}_{tile_id}.png")
    tile_image.save(tile_filename)
    print(f"Сохранена плитка: {tile_filename}")


def split_image_multithreaded(image_path, output_dir, tile_width, tile_height, max_threads=4):

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
                    )
                )
                tile_id += 2048
            tile_row += 2048
            tile_id = 0

        # Ожидаем завершения всех задач
        for task in tasks:
            task.result()

# Пример использования
split_image_multithreaded(
    image_path="image_1_level_0.png",  # Путь к большому изображению
    output_dir="build",    # Папка для сохранения плиток
    tile_width=2048,               # Ширина плитки
    tile_height=2048,              # Высота плитки
    max_threads=12                 # Количество потоков
)
