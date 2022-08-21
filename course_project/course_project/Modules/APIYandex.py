import requests
from loguru import logger

class Yandex:
    def __init__(self, yandex_token):
        logger.info(f"Yandex: Создан объект Yandex - {self}")
        self.url_api = 'https://cloud-api.yandex.net/v1/disk/'
        self.headers = {'Authorization': f'OAuth {yandex_token}', 'Content-Type': 'application/json', 'Accept': 'application/json'}

    def check_floder(self): # Проверка наличии папки "Photo from VK" 
        url = f'{self.url_api}resources'
        params = {'path': '/Photo from VK'}
        response = requests.get(url, params = params, headers= self.headers)
        logger.info(f"Yandex: Проверка наличии папки: {url, params}")
        logger.debug(f"{response}")
        return response.status_code

    def check_floder_json(self): # Достаем JSON загруженных фото 
        url = f'{self.url_api}resources'
        params = {'path': '/Photo from VK'}
        response = requests.get(url, params = params, headers= self.headers)
        logger.info(f"Yandex: JSON загруженных фото: {url, params}")
        logger.debug(f"{response}")
        return response.json()

    def creat_folder_link(self):  # Получить ссылку на создание папки 
        url = f'{self.url_api}resources'
        params = {'path': 'Photo from VK'}
        response = requests.put(url, params = params, headers = self.headers)
        logger.info(f"Yandex: Получить ссылку на создание папки: {url, params}")
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
        logger.info(f"Yandex: Получить ссылку загрузку файлов: {url, params}")
        logger.debug(f"{response}")
        return response.json()

    def put_upload(self, href, filename): # Загрузить файлы по полученной ссылке
        self.href = href
        response = requests.put(self.href, data = open(filename, 'rb'))
        logger.info(f"Yandex: Отправить файл {filename}.jpg на загрузку: {self.href}")
        logger.debug(f"{response}")