import json
import requests
from settings import Credentials, NewPet


class Pets:
    """ API библиотека к сайту http://34.141.58.52:8080/#/"""

    def __init__(self):
        self.base_url = 'http://34.141.58.52:8000/'

    def get_token(self) -> json:
        """Запрос к Swagger сайта для получения уникального токена пользователя по указанным email и password"""
        data = {"email": Credentials.VALID_EMAIL, "password": Credentials.VALID_PASS}
        res = requests.post(self.base_url + 'login', data=json.dumps(data))
        my_token = res.json()['token']
        my_id = res.json()['id']
        status = res.status_code
        return my_token, status, my_id

    """Запрос к Swagger сайта для получения списка пользователей"""
    def get_list_users(self):
        my_token = Pets().get_token()[0]
        headers = {'Authorization': f'Bearer {my_token}'}
        res = requests.get(self.base_url + 'users', headers=headers)
        status = res.status_code
        amount = res.json
        return status, amount

    """Запрос к Swagger сайта для создания питомца пользователя"""
    def post_pet(self):
        my_token = Pets().get_token()[0]
        my_id = Pets().get_token()[2]
        headers = {'Authorization': f'Bearer {my_token}'}
        data = {
            "name": NewPet.NAME, "type": NewPet.TYPE, "age": NewPet.AGE, "owner_id": my_id}
        res = requests.post(self.base_url + 'pet', data=json.dumps(data), headers=headers)
        pet_id = res.json()['id']
        status = res.status_code
        return pet_id, status

    """Запрос к Swagger сайта для добавления фото питомца: вызывается функция создания питомца и ему добавляется фото"""
    def post_pet_photo(self):
        my_token = Pets().get_token()[0]
        pet_id = Pets().post_pet()[0]
        headers = {'Authorization': f'Bearer {my_token}'}
        files = {'pic': ('test.jpg', open('Tests\\Photo\\pet.jpg', 'rb'), 'image/jpg')}
        res = requests.post(self.base_url + f'pet/{pet_id}/image', headers=headers, files=files)
        status = res.status_code
        print(res.json())
        return status

    """Запрос к Swagger сайта для получения списка питомцев пользователя"""
    def get_pets_of_user(self):
        my_token = Pets().get_token()[0]
        my_id = Pets().get_token()[2]
        headers = {'Authorization': f'Bearer {my_token}'}
        data = {"user_id": my_id}
        res = requests.post(self.base_url + 'pets', headers=headers, data=json.dumps(data))
        status = res.status_code
        pets_list = res.json()
        amount = res.json()['total']
        return pets_list, status, amount

    """Запрос к Swagger сайта. Поставить лайк питомцу: создается новый питомец и ему проставляется лайк"""
    def put_like_to_pet(self):
        my_token = Pets().get_token()[0]
        headers = {'Authorization': f'Bearer {my_token}'}
        Pets().post_pet()
        pet_id = Pets().post_pet()[0]
        res = requests.put(self.base_url + f'pet/{pet_id}/like', headers=headers)
        status = res.status_code
        print(status)
        return status

    """Запрос к Swagger сайта. Оставить комментарий о питомце. Если количество питомцев у пользователя  == 0, 
    вызывается функция добавления питомца и добавляется комментарий о нем"""
    def put_comment_to_pet(self):
        my_token = Pets().get_token()[0]
        headers = {'Authorization': f'Bearer {my_token}'}
        if Pets().get_pets_of_user()[2] == 0:
            Pets().post_pet()
        pets_list = Pets().get_pets_of_user()[0]
        pet_id = pets_list["list"][0]["id"]
        message = {"message": "nice pet"}
        res = requests.put(self.base_url + f'pet/{pet_id}/comment', headers=headers, data=json.dumps(message))
        status = res.status_code
        print(status)
        return status

    """Запрос к Swagger сайта. Получить данные о питомце. Если количество питомцев у пользователя  == 0, 
    вызывается функция добавления питомца и получается информация о нем"""
    def get_pet_info(self):
        my_token = Pets().get_token()[0]
        headers = {'Authorization': f'Bearer {my_token}'}
        if Pets().get_pets_of_user()[2] == 0:
            Pets().post_pet()
        pets_list = Pets().get_pets_of_user()[0]
        pet_id = pets_list["list"][0]["id"]
        res = requests.get(self.base_url + f'pet/{pet_id}', headers=headers)
        status = res.status_code
        pet_info = res.json()
        return pet_id, status, pet_info

    """Запрос к Swagger сайта. Изменить данные о питомце (увеличить возраст на 1)"""
    def update_pet_age(self):
        my_token = Pets().get_token()[0]
        headers = {'Authorization': f'Bearer {my_token}'}
        if Pets().get_pets_of_user()[2] == 0:
            Pets().post_pet()
        pet_info = Pets().get_pet_info()[2]
        pet_info['pet']['age'] = pet_info['pet']['age'] + 1
        res = requests.patch(self.base_url + 'pet', headers=headers, data=json.dumps(pet_info['pet']))
        status = res.status_code
        print(status)
        return status

    """Запрос к Swagger сайта. Удалить питомца. Если количество питомцев у пользователя  == 0, вызывается функция 
    добавления питомца, после чего он удаляется"""

    def delete_pet(self):
        my_token = Pets().get_token()[0]
        headers = {'Authorization': f'Bearer {my_token}'}
        if Pets().get_pets_of_user()[2] == 0:
            Pets().post_pet()
        pets_list = Pets().get_pets_of_user()[0]
        pets_count_before = Pets().get_pets_of_user()[2]
        pet_id = pets_list["list"][0]["id"]
        res = requests.delete(self.base_url + f'pet/{pet_id}', headers=headers)
        pets_count_after = pets_list['total']
        status = res.status_code
        return status, pets_count_before, pets_count_after

    """Запрос к Swagger сайта. Функция для удаления всех питомцев после проведения тестов"""
    def delete_all_pets(self):
        my_token = Pets().get_token()[0]
        headers = {'Authorization': f'Bearer {my_token}'}
        pets_list = Pets().get_pets_of_user()[0]
        pets_count = Pets().get_pets_of_user()[2]
        print(pets_list)
        print(pets_count)
        for i in pets_list['list']:
            pet_id = i["id"]
            res = requests.delete(self.base_url + f'pet/{pet_id}', headers=headers)
            print(Pets().get_pets_of_user()[2])
        status = res.status_code
        return status

# Pets().get_token()
# Pets().get_pets_of_user()
# Pets().put_like_to_pet()
# Pets().put_comment_to_pet()
# Pets().get_pet_info()

# Pets().update_pet_age()
# Pets().delete_pet()
# Pets().get_list_users()
# Pets().post_pet()
# Pets().post_pet_photo()
Pets().delete_all_pets()
