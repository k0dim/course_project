from pprint import pprint
import requests
import os
from loguru import logger
import json


class VK:
    def __init__(self, access_token, user_id, version ='5.131'):
        logger.info(f"VK: Создать объект VK - {self}")
        self.token = access_token
        self.id = user_id
        self.version = version
        self.params = {'access_token': self.token, 'v': self.version}

    def photos_get(self, count): # Получение фото из ВК 
        self.count = count 
        url = 'https://api.vk.com/method/photos.get'
        params = {'user_id': self.id, 'album_id': 'profile', 'extended': 1, 'photo_sizes': 1, 'count': {self.count}}
        response = requests.get(url, params={**self.params, **params})
        logger.info(f"VK: Получить фотографии из VK - {self}: {url, params}")
        logger.debug(f"{response}")
        return response.json()

class Yandex:
    def __init__(self, yandex_token):
        logger.info(f"Yandex: Создан объект Yandex - {self}")
        self.url_api = 'https://cloud-api.yandex.net/v1/disk/'
        self.headers = {'Authorization': f'OAuth {yandex_token}', 'Content-Type': 'application/json', 'Accept': 'application/json'}

    def check_floder(self): # Проверка наличии папки "Photo from VK" 
        url = f'{self.url_api}resources'
        params = {'path': '/Photo from VK'}
        response = requests.get(url, params = params, headers= self.headers)
        return response.status_code

    def check_floder_json(self): # Достаем JSON загруженных фото 
        url = f'{self.url_api}resources'
        params = {'path': '/Photo from VK'}
        response = requests.get(url, params = params, headers= self.headers)
        return response.json()

    def creat_folder_link(self):  # Получить ссылку на создание папки 
        url = f'{self.url_api}resources'
        params = {'path': 'Photo from VK'}
        response = requests.put(url, params = params, headers = self.headers)
        logger.info(f"Yandex: Получить ссылку на создание папки: {url, params, self.headers}")
        logger.debug(f"{response}")
        return response.json()

    def creat_folder(self, href_folder): # Создать папку
        self.href_folder = href_folder
        response = requests.put(self.href_folder)
        logger.info(f"Yandex: Создание папки - {self}: {self.href_folder}")
        logger.debug(f"{response}")

    def get_linc_upload(self, file_path): # Получить ссылку на загрузку файлов
        url = f'{self.url_api}resources/upload'
        params = {'path': file_path, 'overwrite': 'true'}
        response = requests.get(url, params = params, headers = self.headers)
        logger.info(f"Yandex: Получить ссылку загрузку файлов: {url, params, self.headers}")
        logger.debug(f"{response}")
        return response.json()

    def put_upload(self, href, filename): # Загрузить файлы по полученной ссылке
        self.href = href
        response = requests.put(self.href, data = open(filename, 'rb'))
        logger.info(f"Yandex: Отправить файл {filename}.jpg на загрузку: {self.href}")
        logger.debug(f"{response}")


def server_photo(): # Функция получает фото из ВК, сохраняяет в папку и переименовывает
    json_photo = vk.photos_get(count_photo)
    for json_photo_list in json_photo['response']['items']:
        likes = json_photo_list['likes']
        for json_photo_dict in json_photo_list['sizes']:
            if json_photo_dict['type'] == 'z':
                namefile = likes['count']
                FILE_NAME = f'likes_{namefile}.jpg'
                full_path = os.path.join(ROAD, CP, DIR_NAME, FILE_NAME)
                img = requests.get(f"{json_photo_dict['url']}")
                with open(full_path, 'bw') as img_file:
                    img_file.write(img.content)
                logger.info(f"System: Отправка {namefile}.jpg на Диск")
    return

def floder(): # Функция проверки на наличие папки, в случае ее отсутствии создает папку (избежание 403)
    if ya.check_floder() == 404:
        logger.info("System: Запуск создания папки")
        link = ya.creat_folder_link()
        pprint(link['href'])
        href_folder = link['href']
        ya.creat_folder(href_folder)
    elif ya.check_floder() == 200:
        logger.info("System: Папка 'Photo from VK' присутствует на Диске. Запись в существующую папку.")

def upload_photo(): # Функция, которая загружает файлы в папку на Диске
    logger.info("System: Запуск загрузки файлов")
    for filename in os.listdir(full_path):
        if filename.endswith(".jpg"): 
            link_dir = ya.get_linc_upload(f'Photo from VK/{filename}')
            href = link_dir['href']
            ya.put_upload(href, os.path.join(full_path, filename))
            logger.info(f"System: Загрузка {filename}.jpg на диск")
            continue
        else:
            continue

def user_token_():
    token = {}
    token['access_token'] = input('Укажите токен авторизации API VK: ')
    token['user_id'] = input('Укажите ID пользователя: ')
    token['yandex_token'] = input('Укажите токен авторизации API Яндекс: ')
    logger.info(f"Создан словарь с авторизацонными данными {token}")
    return token

if __name__ == '__main__':
    # Общие переменные и настройка логирования
    logger.info("Запуск работы")
    ROAD = os.getcwd() 
    CP = 'course_project'
    DIR_NAME = 'photo'
    LOG_NAME = 'file.log'
    JSON_NAME = 'photo.json'
    full_path = os.path.join(ROAD, CP, DIR_NAME)
    full_path_log = os.path.join(ROAD, CP, LOG_NAME)
    full_path_json = os.path.join(ROAD, CP, JSON_NAME)
    logger.add(full_path_log, format="{time} {level} {message}", level="INFO")
    logger.add(full_path_log, format="{time} {level} {message}", level="DEBUG")
    # Авторизация
    print('Необходима авторизация в ВК и Яндекс')
    token = user_token_()
    vk = VK(token['access_token'], token['user_id'])
    ya = Yandex(token['yandex_token'])
    count_photo = input('Укажите количество фотографий: ')
    # Выполнение програмьы
    server_photo() # - Выгружаем фото из ВК
    floder() # - Проверяем/Создаем папку на Диске
    upload_photo() # - Загружаем фото на Диск
    # Создание файла JSON с заргуженными файлами
    with open(full_path_json, 'w') as json_file:
        a = ya.check_floder_json()
        b = str(a)
        json.dump(ya.check_floder_json(), json_file, sort_keys=True, indent=2)