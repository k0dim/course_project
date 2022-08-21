from pprint import pprint
import requests
import os
from loguru import logger
import json

from Modules.APIYandex import Yandex
from Modules.APIVK import VK


def server_photo(): # Функция получает фото из ВК, сохраняяет в папку и переименовывает
    json_photo = vk.photos_get(count_photo)
    for json_photo_list in json_photo['response']['items']:
        likes = json_photo_list['likes']
        json_photo_dict = json_photo_list['sizes'][len(json_photo_list['sizes']) -1]
        namefile = likes['count']
        FILE_NAME = f'likes_{namefile}.jpg'
        full_path = os.path.join(ROAD, 'course_project', 'photo', FILE_NAME)
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
    token['access_token'] = 'vk1.a.AQESOww6q6owUGK3yymgrKFAFp09opAf_-bxcTKvEZxNHCpb2qWsloOGkJt09DBtFvRM2BD0Zght0Cuzhr5uvpYYHuJ10BElQPFGPaTQxmKzB98H13VSnEdc0rD4j81MDiFTODxZ2My1Kb7YoZmAyhAIN5Oe7AD9ull1LHUEFCZcpEwSWktRYwjEs6QebVAE' #input('Укажите токен авторизации API VK: ')
    token['user_id'] = '265164484' #input('Укажите ID пользователя: ')
    token['yandex_token'] = 'AQAAAAATf-PhAADLW50Lxq76NkyFhElSEL_l-oo' #input('Укажите токен авторизации API Яндекс: ')
    logger.info(f"Создан словарь с авторизацонными данными")
    return token

if __name__ == '__main__':
    # Общие переменные и настройка логирования
    logger.info("Запуск работы")
    ROAD = os.getcwd() 
    full_path = os.path.join(ROAD, 'course_project', 'photo')
    full_path_log = os.path.join(ROAD, 'course_project', 'file.log')
    full_path_json = os.path.join(ROAD, 'course_project', 'photo.json')
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
        json.dump(ya.check_floder_json(), json_file, sort_keys=True, indent=2)
