# Название урока: Параметризованный тест
import json
from http.client import responses

import httpx
import pytest
from jsonschema import validate
from matplotlib.font_manager import json_load

from core.contracts import REGISTERED_USER_SCHEME

BASE_URL = "https://reqres.in/"
REGISTER_USER = "api/register"
REGISTER_UNSUCCESSFUL_USER = "api/register"
LOGIN_USER = "api/login"

# Открываем созданный JSON-файл
json_file = open('/Users/apple/PycharmProjects/MyApiTests/core/new_user_data.json')
# Загружаем этот файл
json_data = json.load(json_file)


# Это декоратор из библиотеки pytest, который позволяет запускать тестовую
# функцию test_successful_user несколько раз с разными значениями параметра json_data.
# Анотоция позволит запустить test_successful_user несколькол раз с разными значениями параметра json_data
# Второе json_data - это данные из файла, тоесть значения для 'json_data'
@pytest.mark.parametrize('json_data', json_data)
def test_successful_user(json_data):
    response = httpx.post(BASE_URL + REGISTER_USER, json=json_data)

    # Проверяем, что статус код - 200
    assert response.status_code == 200
    # Проверяем JSON в ответе
    validate(response.json(), REGISTERED_USER_SCHEME)


# Мои тесты

# Файл с неудачными данными пользователя
json_file_with_invalid_data = open('/Users/apple/PycharmProjects/MyApiTests/core/invalid_user_data.json')
json_data2 = json.load(json_file_with_invalid_data)

# Тест на проверку неудачной регистрации
@pytest.mark.parametrize('json_data2', json_data2)
def test_register_unsuccessful_user(json_data2):
    response = httpx.post(BASE_URL + REGISTER_UNSUCCESSFUL_USER, json=json_data2)

    # Проверяем, что статус код - 400
    assert response.status_code == 400

# Файл  c данными для авторизации пользователя
json_file_login_user = open('/Users/apple/PycharmProjects/MyApiTests/core/login_user.json')
json_data3 = json.load(json_file_login_user)
@pytest.mark.parametrize('json_data3', [json_data3])
def test_login_user(json_data3):
    response = httpx.post(BASE_URL + LOGIN_USER, json=json_data3)

    # Проверка статуса ответа
    assert response.status_code == 200

    print(response.text)
