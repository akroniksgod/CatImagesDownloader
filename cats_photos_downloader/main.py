import requests
from bs4 import BeautifulSoup as BS
import os


def get_cat_images():
    # Ссылка на страницу с информацией о котиках в википедии
    wiki_url = "https://ru.wikipedia.org/wiki/%D0%9A%D0%BE%D1%82"

    try:
        # Загрузка страницы с информацией о котиках
        response = requests.get(wiki_url)
        soup = BS(response.content, 'html.parser')

        # Поиск всех изображений на странице
        images = soup.find_all('img')

        # Фильтрация изображений, оставляем только те, которые относятся к котикам
        cat_images = ["https:" + img['src'] for img in images if img.has_attr('alt') and "кот" in img['alt'].lower()]

        # Возвращаем список ссылок на изображения котиков
        return cat_images
    except (AttributeError, ConnectionError) as e:
        import sys
        print("Ошибка при получении изображений котиков:", e, file=sys.stderr)
        return []


def download_images(image_urls, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for i, image_url in enumerate(image_urls):
        try:
            response = requests.get(image_url)
            filename = os.path.join(output_folder, f"cat_image_{i}.jpg")
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"Изображение {i + 1}/{len(image_urls)} загружено: {filename}")
        except Exception as e:
            print(f"Ошибка при загрузке изображения {i + 1}: {e}")


if __name__ == '__main__':
    cat_images = get_cat_images()
    output_folder = "cat_images"
    download_images(cat_images, output_folder)
