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

# Файл с данными пользователя для регистрации
json_file = open('/Users/apple/PycharmProjects/MyApiTests/core/new_user_data.json')
json_data = json.load(json_file)

@pytest.mark.parametrize('json_data', json_data)
def test_successful_user(json_data):
    response = httpx.post(BASE_URL + REGISTER_USER, json=json_data)
    assert response.status_code == 200
    validate(response.json(), REGISTERED_USER_SCHEME)

# Файл с неудачными данными пользователя для регистрации
json_file_with_invalid_data = open('/Users/apple/PycharmProjects/MyApiTests/core/invalid_user_data.json')
json_data_register_user = json.load(json_file_with_invalid_data)

# Тест на проверку неудачной регистрации:Неудачная, так как передается только логин: почта, пароль не передается
@allure.suite('Проверки регистрации пользователя')
@allure.title('Тест1:Проверка сценария на неаудачную регистрацию пользователя')
@pytest.mark.parametrize('json_data_parametr', json_data_register_user)
def test_register_user_unsuccessful(json_data_parametr):
    #Обозначаем шаг в allure-отчете
    with allure.step(f'Делаем запрос по адресу: {BASE_URL + REGISTER_UNSUCCESSFUL_USER}'):
        try:
            #Собираем URL и определяем тип запроса
            response = httpx.post(BASE_URL + REGISTER_UNSUCCESSFUL_USER, json=json_data_parametr)
        except httpx.HTTPStatusError as e:
            #Выводим сообщение об ошибке,если запрос не прошел
            print(f"Ошибка HTTP: {e.response.status_code} - {e.response.text}")
    # Обозначаем шаг в allure-отчете
    with allure.step('Проверяем код ответа 400'):
        try:
            #Проверяем статус код ответа
            assert response.status_code == 400, f"Ожидали статус код 400, а получили {response.status_code}"
        except AssertionError as e:
            allure.attach(str(e), name="Ошибка проверки статуса", attachment_type=allure.attachment_type.TEXT)

# Файл с данными пользователя для авторизации
json_file_login_user = open('/Users/apple/PycharmProjects/MyApiTests/core/login_user.json')
json_data_login_user = json.load(json_file_login_user)
# Тест на проверку авторизации пользователя
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
            # Проверка data на пустоту
            if not data:
                raise ValueError("Переменная data пустая!")
        except ValueError:
            assert False, 'Ответ JSON пустой'

    with allure.step('Проверяем схему ответа с заданным в contract шаблоном по имени USER_REGISTER_DATA_SCHEME'):
        try:
            validate(data, USER_REGISTER_DATA_SCHEME)
        except Exception as e:
            allure.attach(str(e), name="Ошибка при валидации", attachment_type=allure.attachment_type.TEXT)

#В тесте показывается передача, например, заголовков в тесте
@pytest.mark.parametrize('users_data',user_data)
def test_successful_register(users_data):
    headers = {'Content-Type': 'application/json'}
    response = httpx.post(BASE_URL+REGISTER_USER,json=users_data,headers=headers)
    print(users_data)
    assert response.status_code == 200
    validate(response.json(),REGISTERED_USER_SCHEME)

#В тесте показывается использование задержки при обработке ответа от сервера
#timeout - это то время,которое мы ждем перед тем,как завершить выполнение запроса
#Вариант использования 1:timeout используем,например, когда видим,что тест выполняется долго
#Вариант  использования 2:Например,запрос который мы тестируем должен выполняться 2 секунды
# и значит мы ставим в автотесте timeout и потом в отчете увидим,что тест выполняется больше 4-х сек
def test_deleyed_user_list():
    response = httpx.get(BASE_URL+DELAYED_REQUEST,timeout=4)
    assert response.status_code == 200
