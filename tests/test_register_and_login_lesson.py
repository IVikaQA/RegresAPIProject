import json
import httpx
import pytest
from jsonschema import validate
import allure
from core.contracts import REGISTERED_USER_SCHEME
from core.contracts import USER_REGISTER_DATA_SCHEME

BASE_URL = 'https://reqres.in/'
REGISTER_USER = 'api/register'
REGISTER_UNSUCCESSFUL_USER = 'api/register'
LOGIN_USER = 'api/login'

json_file = open('/Users/apple/PycharmProjects/MyApiTests/core/new_user_data.json')
json_data = json.load(json_file)

@pytest.mark.parametrize('json_data', json_data)
def test_successful_user(json_data):
    response = httpx.post(BASE_URL + REGISTER_USER, json=json_data)
    assert response.status_code == 200
    validate(response.json(), REGISTERED_USER_SCHEME)

json_file_with_invalid_data = open('/Users/apple/PycharmProjects/MyApiTests/core/invalid_user_data.json')
json_data_register_user = json.load(json_file_with_invalid_data)

@allure.suite('Проверки регистрации пользователя')
@allure.title('Тест1:Проверка сценария на неаудачную регистрацию пользователя')
@pytest.mark.parametrize('json_data_parametr', json_data_register_user)
def test_register_user_unsuccessful(json_data_parametr):
    with allure.step(f'Делаем запрос по адресу: {BASE_URL + REGISTER_UNSUCCESSFUL_USER}'):
        try:
            response = httpx.post(BASE_URL + REGISTER_UNSUCCESSFUL_USER, json=json_data_parametr)
        except httpx.HTTPStatusError as e:
            print(f"Ошибка HTTP: {e.response.status_code} - {e.response.text}")

    with allure.step('Проверяем код ответа 400'):
        try:
            assert response.status_code == 400, f"Ожидали статус код 400, а получили {response.status_code}"
        except AssertionError as e:
            allure.attach(str(e), name="Ошибка проверки статуса", attachment_type=allure.attachment_type.TEXT)

json_file_login_user = open('/Users/apple/PycharmProjects/MyApiTests/core/login_user.json')
json_data_login_user = json.load(json_file_login_user)
@allure.suite('Проверки авторизации пользователя')
@allure.title("Тест2:Проверка сценария на удачную авторизацию пользователя")
@pytest.mark.parametrize('json_data_parametr', [json_data_login_user])
def test_login_user(json_data_parametr):
    with allure.step(f'Делаем запрос по адресу: {BASE_URL + LOGIN_USER}'):
        try:
            response = httpx.post(BASE_URL + LOGIN_USER, json=json_data_parametr)
        except httpx.HTTPStatusError as e:
            print(f"Ошибка HTTP: {e.response.status_code} - {e.response.text}")

    with allure.step('Проверяем,что код ответа - 200'):
        try:
            assert response.status_code == 200, f"Ожидали статус код 200, а получили {response.status_code}"
        except AssertionError as e:
            allure.attach(str(e), name="Ошибка проверки статуса", attachment_type=allure.attachment_type.TEXT)

    with allure.step('Проверяем,что ответ не пустой'):
        try:
            data = response.json()
        # и тест завершится с сообщением "Ответ JSON пустой".
        except ValueError:
            assert False, 'Ответ JSON пустой'

    with allure.step('Проверяем схему ответа с заданным в contract шаблоном по имени USER_REGISTER_DATA_SCHEME'):
        try:
            validate(data, USER_REGISTER_DATA_SCHEME)
        except Exception as e:
            allure.attach(str(e), name="Ошибка при валидации", attachment_type=allure.attachment_type.TEXT)