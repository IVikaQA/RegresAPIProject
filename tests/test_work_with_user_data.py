# Здесь автотесты на методы POST:CREATE,
from http.client import responses

import httpx
from jsonschema import validate
from core.contracts import CREATE_USER_SCHEME
from core.contracts import UPDATE_USER_SCHEME
import datetime

BASE_URL = "https://reqres.in/"
CREATE_USER = "api/users"
PUT_USER = "api/users/2"


# Метод 1
def test_create_user_with_name_and_job():
    # Взяли тело из 'SWAGER'
    body = {
        "name": "morpheus",
        "job": "leader"
    }
    # Собираем POST-запрос
    response = httpx.post(BASE_URL + CREATE_USER, json=body)
    print(response.json())
    assert response.status_code == 201
    response_json = response.json()

    # Работаем с датой
    # Заодно убираем из строки букву T
    creation_date = response_json['createdAt'].replace('T', ' ')
    # Метод utcnow устарел и поэтому строка закоменчена
    # current_date = str(datetime.datetime.utcnow())
    # Чтобы сравнивать перменнные с датами,нужно обе переменные привести к типу str
    current_date = str(datetime.datetime.now(datetime.UTC))

    # ПРОВЕРКИ
    validate(response_json, CREATE_USER_SCHEME)
    # Проверяем, что в json-ответа есть поле name, которое мы передавали в запросе
    assert (response_json['name'] == body['name'])
    assert (response_json['job'] == body['job'])
    # [0:16] - это диапазон,тоесть сколько нужно символов взять из строки?
    assert creation_date[0:16] == current_date[0:16]


# Метод 2
def test_create_user_without_name():
    # Взяли тело из 'SWAGER'
    body = {
        "job": "leader"
    }
    # Собираем POST-запрос
    response = httpx.post(BASE_URL + CREATE_USER, json=body)
    print(response.json())
    assert response.status_code == 201
    response_json = response.json()

    # Работаем с датой
    # Заодно убираем из строки букву T
    creation_date = response_json['createdAt'].replace('T', ' ')
    # Метод utcnow устарел и поэтому строка закоменчена
    # current_date = str(datetime.datetime.utcnow())
    # Чтобы сравнивать перменнные с датами,нужно обе переменные привести к типу str
    current_date = str(datetime.datetime.now(datetime.UTC))

    # ПРОВЕРКИ
    validate(response_json, CREATE_USER_SCHEME)
    # Проверяем, что в json-ответа есть поле name, которое мы передавали в запросе
    assert (response_json['job'] == body['job'])
    # [0:16] - это диапазон,тоесть сколько нужно символов взять из строки?
    assert creation_date[0:16] == current_date[0:16]


# Метод 3
def test_create_user_without_name():
    # Взяли тело из 'SWAGER'
    body = {
        "job": "leader"
    }
    # Собираем POST-запрос
    response = httpx.post(BASE_URL + CREATE_USER, json=body)
    print(response.json())
    assert response.status_code == 201
    response_json = response.json()

    # Работаем с датой
    # Заодно убираем из строки букву T
    creation_date = response_json['createdAt'].replace('T', ' ')
    # Метод utcnow устарел и поэтому строка закоменчена
    # current_date = str(datetime.datetime.utcnow())
    # Чтобы сравнивать перменнные с датами,нужно обе переменные привести к типу str
    current_date = str(datetime.datetime.now(datetime.UTC))

    # ПРОВЕРКИ
    validate(response_json, CREATE_USER_SCHEME)
    # Проверяем, что в json-ответа есть поле name, которое мы передавали в запросе
    assert (response_json['job'] == body['job'])
    # [0:16] - это диапазон,тоесть сколько нужно символов взять из строки?
    assert creation_date[0:16] == current_date[0:16]


# Меетод 4
def test_create_user_without_job():
    # Взяли тело из 'SWAGER'
    body = {
        "name": "morpheus"
    }
    # Собираем POST-запрос
    response = httpx.post(BASE_URL + CREATE_USER, json=body)
    print(response.json())
    assert response.status_code == 201
    response_json = response.json()

    # Работаем с датой
    # Заодно убираем из строки букву T
    creation_date = response_json['createdAt'].replace('T', ' ')
    # Метод utcnow устарел и поэтому строка закоменчена
    # current_date = str(datetime.datetime.utcnow())

    # Получаем текущую дату и время
    # Чтобы сравнивать перменнные с датами,нужно обе переменные привести к типу str
    current_date = str(datetime.datetime.now(datetime.UTC))

    # ПРОВЕРКИ
    validate(response_json, CREATE_USER_SCHEME)
    # Проверяем, что в json-ответа есть поле name, которое мы передавали в запросе
    assert (response_json['name'] == body['name'])
    # [0:16] - это диапазон,тоесть сколько нужно символов взять из строки?
    assert creation_date[0:16] == current_date[0:16]


# Мои методы
# Тест на проверкк метода PUT
def test_put_in_data_user():
    body = {
        "name": "morpheus",
        "job": "zion resident"
    }

    # Собираем запрос
    response = httpx.put(BASE_URL + PUT_USER, json=body)
    # print('Ваш ответ: '+ response.text)

    response_json = response.json()

    # Убираем из строки букву T
    creation_date = response_json['updatedAt'].replace('T', ' ')
    current_date = str(datetime.datetime.now(datetime.UTC))

    # ПРОВЕРКИ
    # Проверяем статус код ответа
    assert response.status_code == 200
    # Проверяем соответствие ответа на запрос схеме
    validate(response_json, UPDATE_USER_SCHEME)
    # Проверяем, что в ответе есть поле name
    assert 'name' in response_json
    # Проверяем, что в ответе есть поле name
    assert 'job' in response_json
    # [0:16] - это диапазон,тоесть сколько нужно символов взять из строки?
    assert creation_date[0:16] == current_date[0:16]


# Тест на проверку метода PUT:Проверяем обазателен ли параметр name
def test_put_in_data_user_without_name():
    body = {
        "job": "zion resident"
    }

    # Собираем запрос
    response = httpx.put(BASE_URL + PUT_USER, json=body)
    # print('Ваш ответ: '+ response.text)

    response_json = response.json()

    # Убираем из строки букву T
    creation_date = response_json['updatedAt'].replace('T', ' ')
    current_date = str(datetime.datetime.now(datetime.UTC))

    # ПРОВЕРКИ
    # Проверяем статус код ответа
    assert response.status_code == 200
    # Проверяем соответствие ответа на запрос схеме
    validate(response_json, UPDATE_USER_SCHEME)
    # Проверяем, что в ответе есть поле job
    assert 'job' in response_json
    # Проверяем, что в ответе нет поля name
    assert 'name' not in response_json
    # [0:16] - это диапазон,тоесть сколько нужно символов взять из строки?
    assert creation_date[0:16] == current_date[0:16]


# Тест на проверку метода PUT:Проверяем обазателен ли параметр job
def test_put_in_data_user_without_job():
    body = {
        "name": "morpheus"
    }

    # Собираем запрос
    response = httpx.put(BASE_URL + PUT_USER, json=body)
    print('Ваш ответ: ' + response.text)

    response_json = response.json()

    # Убираем из строки букву T
    creation_date = response_json['updatedAt'].replace('T', ' ')
    current_date = str(datetime.datetime.now(datetime.UTC))

    # ПРОВЕРКИ
    # Проверяем статус код ответа
    assert response.status_code == 200
    # Проверяем соответствие ответа на запрос схеме
    validate(response_json, UPDATE_USER_SCHEME)
    # Проверяем, что в ответе нет поля job
    assert 'job' not in response_json
    # Проверяем, что в ответе есть поле name
    assert 'name' in response_json
    # [0:16] - это диапазон,тоесть сколько нужно символов взять из строки?
    assert creation_date[0:16] == current_date[0:16]


# Тест на проверку метода patch
def test_patch_in_data_user():
    body = {
        "name": "morpheus",
        "job": "zion resident"
    }

    # Собираем запрос
    response = httpx.patch(BASE_URL + PUT_USER, json=body)
    print('Ваш ответ: ' + response.text)

    response_json = response.json()

    # Убираем из строки букву T
    creation_date = response_json['updatedAt'].replace('T', ' ')
    current_date = str(datetime.datetime.now(datetime.UTC))

    # ПРОВЕРКИ
    # Проверяем статус код ответа
    assert response.status_code == 200
    # Проверяем соответствие ответа на запрос схеме
    validate(response_json, UPDATE_USER_SCHEME)
    # Проверяем, что в ответе нет поля name
    assert 'name' in response_json
    # Проверяем, что в ответе нет поля job
    assert 'job' in response_json
    # [0:16] - это диапазон,тоесть сколько нужно символов взять из строки?
    assert creation_date[0:16] == current_date[0:16]


# Тест на проверку метода patch:Обязателен ли параметр name
def test_patch_in_data_user_without_name():
    body = {
        "job": "zion resident"
    }

    # Собираем запрос
    response = httpx.patch(BASE_URL + PUT_USER, json=body)
    print('Ваш ответ: ' + response.text)

    response_json = response.json()

    # Убираем из строки букву T
    creation_date = response_json['updatedAt'].replace('T', ' ')
    current_date = str(datetime.datetime.now(datetime.UTC))

    # ПРОВЕРКИ
    # Проверяем статус код ответа
    assert response.status_code == 200
    # Проверяем соответствие ответа на запрос схеме
    validate(response_json, UPDATE_USER_SCHEME)
    # Проверяем, что в ответе есть поле job
    assert 'job' in response_json
    # Проверяем, что в ответе нет поля name
    assert 'name' not in response_json
    # [0:16] - это диапазон,тоесть сколько нужно символов взять из строки?
    assert creation_date[0:16] == current_date[0:16]


# Тест на проверку метода patch:Обязателен ли параметр name
def test_patch_in_data_user_without_job():
    body = {
        "name": "morpheus"
    }

    # Собираем запрос
    response = httpx.patch(BASE_URL + PUT_USER, json=body)
    print('Ваш ответ: ' + response.text)

    response_json = response.json()

    # Убираем из строки букву T
    creation_date = response_json['updatedAt'].replace('T', ' ')
    current_date = str(datetime.datetime.now(datetime.UTC))

    # ПРОВЕРКИ
    # Проверяем статус код ответа
    assert response.status_code == 200
    # Проверяем соответствие ответа на запрос схеме
    validate(response_json, UPDATE_USER_SCHEME)
    # Проверяем, что в ответе есть поле job
    assert 'name' in response_json
    # Проверяем, что в ответе нет поля job
    assert 'job' not in response_json
    # [0:16] - это диапазон,тоесть сколько нужно символов взять из строки?
    assert creation_date[0:16] == current_date[0:16]


# Тест на проверку метода DELETE
def test_delete_user():
    response = httpx.delete(BASE_URL + PUT_USER)
    # Проверка-1
    assert response.status_code == 204
