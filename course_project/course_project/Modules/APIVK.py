import requests
from loguru import logger

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