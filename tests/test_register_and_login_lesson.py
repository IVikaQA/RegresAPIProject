# Название урока: Параметризованный тест
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

# Открываем созданный JSON-файл
json_file = open('/Users/apple/PycharmProjects/MyApiTests/core/new_user_data.json')
# Загружаем этот файл
json_data = json.load(json_file)


# 'json_data' это название параметра который мы используем в тесте
# А json_data это данные, которые мы передаем в тест
@pytest.mark.parametrize('json_data', json_data)
def test_successful_user(json_data):
    response = httpx.post(BASE_URL + REGISTER_USER, json=json_data)

    # Проверяем, что статус код - 200
    assert response.status_code == 200
    # Проверяем JSON в ответе
    validate(response.json(), REGISTERED_USER_SCHEME)

#Мои тесты
# Файл с неудачными данными пользователя
json_file_with_invalid_data = open('/Users/apple/PycharmProjects/MyApiTests/core/invalid_user_data.json')
json_data_register_user = json.load(json_file_with_invalid_data)

@allure.suite('Проверки регистрации пользователя')
@allure.title('Тест1:Проверка сценария на неаудачную регистрацию пользователя')
# Тест на проверку неудачной регистрации
@pytest.mark.parametrize('json_data_parametr', json_data_register_user)
def test_register_user_unsuccessful(json_data_parametr):
    # Проверка-1
    with allure.step(f'Делаем запрос по адресу: {BASE_URL + REGISTER_UNSUCCESSFUL_USER}'):
        try:
            response = httpx.post(BASE_URL + REGISTER_UNSUCCESSFUL_USER, json=json_data_parametr)
        except httpx.HTTPStatusError as e:
            print(f"Ошибка HTTP: {e.response.status_code} - {e.response.text}")

    # Вывод ответа
    #print(response.text)

    #Проверка-2:Проверка статуса ответа 400
    with allure.step('Проверяем код ответа 400'):
        try:
            assert response.status_code == 400, f"Ожидали статус код 400, а получили {response.status_code}"
        except AssertionError as e:
            allure.attach(str(e), name="Ошибка проверки статуса", attachment_type=allure.attachment_type.TEXT)


# Файл  c данными для авторизации пользователя
json_file_login_user = open('/Users/apple/PycharmProjects/MyApiTests/core/login_user.json')
json_data_login_user = json.load(json_file_login_user)
@allure.suite('Проверки авторизации пользователя')
@allure.title("Тест2:Проверка сценария на удачную авторизацию пользователя")
@pytest.mark.parametrize('json_data_parametr', [json_data_login_user])
def test_login_user(json_data_parametr):
    #Проверка-1
    with allure.step(f'Делаем запрос по адресу: {BASE_URL + LOGIN_USER}'):
        try:
            response = httpx.post(BASE_URL + LOGIN_USER, json=json_data_parametr)
        except httpx.HTTPStatusError as e:
            print(f"Ошибка HTTP: {e.response.status_code} - {e.response.text}")
    #Вывод ответа
    #print(response.text)

    #Проверка-2
    with allure.step('Проверяем,что код ответа - 200'):
        try:
            assert response.status_code == 200, f"Ожидали статус код 200, а получили {response.status_code}"
        except AssertionError as e:
            allure.attach(str(e), name="Ошибка проверки статуса", attachment_type=allure.attachment_type.TEXT)

    #Проверка-3
    with allure.step('Проверяем,что ответ не пустой'):
        try:
            #Подготавливаем данные для будующих проверок
            data = response.json()
        #Обработка исключения: Если ответ пришел пустой, то будет вызвано исключение,
        # и тест завершится с сообщением "Ответ JSON пустой".
        except ValueError:
            assert False, 'Ответ JSON пустой'

    #Проверка-4
    with allure.step('Проверяем схему ответа с заданным в contract шаблоном по имени USER_REGISTER_DATA_SCHEME'):
        try:
            validate(data, USER_REGISTER_DATA_SCHEME)
        except Exception as e:
            allure.attach(str(e), name="Ошибка при валидации", attachment_type=allure.attachment_type.TEXT)