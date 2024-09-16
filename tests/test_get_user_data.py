from cgitb import reset
from http.client import responses
from idlelib.rpc import RPCProxy

import httpx
from jsonschema import validate

from core.contracts import USER_DATA_SCHEME

BASE_URL = "https://reqres.in/"
LIST_USERS = "api/users?page=2"
SINGLE_USER = "api/users/2"
NOT_FOUND_USER = "api/users/23"
EMAIL_ENDS = "@reqres.in"
AVATAR_ENDS = "-image.jpg"


# Пишем проверки на метод LIST USERS сайта https://reqres.in
def test_list_users():
    response = httpx.get(BASE_URL + LIST_USERS)
    # 1)Проверка,что код ответа - 200
    assert response.status_code == 200

    # Выводим ответ от сервера
    # print(response.text)
    # Подготовка для других проверок ниже.Берем часть ответа
    data = response.json()['data']

    # 2)Проверка схемы с помощью функции validate
    # Порядок: 1-ый параметры - Что проверяем; 2-ой параметр - С чем сравниваем ответ
    # Проходят по каждому пользователю из списка.
    for item in data:
        # Проверяют, соответствует ли каждый пользователь заданной схеме.
        validate(item, USER_DATA_SCHEME)
        # Проверяют, имеет ли электронная почта правильный домен.
        assert item['email'].endswith(EMAIL_ENDS)

    # 3) Проверка того, что ID,которое приходит в ответе, содержится в аватаре,в конце названия файла
    assert item['avatar'].endswith(str(item['id']) + AVATAR_ENDS)


# Пишем проверки на метод SINGLE USER сайта https://reqres.in
def test_single_user():
    response = httpx.get(BASE_URL + SINGLE_USER)
    # 1)Проверка,что код ответа - 200
    assert response.status_code == 200
    # Подготовка для слудующих проверок в методе
    data = response.json()['data']
    #print(response.json()['support'])

    assert data['email'].endswith(EMAIL_ENDS)
    assert data['avatar'].endswith(str(data['id']) + AVATAR_ENDS)


# Пишем проверки на метод SINGLE USER NOT FOUND сайта https://reqres.in
def test_user_not_found():
    response = httpx.get(BASE_URL + NOT_FOUND_USER)
    # 1)Проверка,что код ответа - 404
    assert response.status_code == 404
