import httpx
from jsonschema import validate
import matplotlib.colors as mcolors
from core.contracts import USER_DATA_SCHEME
from core.contracts2 import USER_DATA_SCHEME2

BASE_URL = "https://reqres.in/"
LIST_USERS = "api/users?page=2"
LIST = "api/unknown"
SINGLE_USER = "api/users/2"
SINGLE = "api/unknown/2"
SINGLE_RESOURCES = "api/unknown/"
NOT_FOUND_USER = "api/users/23"
NOT_FOUND_SINGLE_RESOURCES = "api/unknown/23"
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
        # 3)Проверка того,что каждый пользователь(item) из ответа соответствует заданной схеме
        validate(item, USER_DATA_SCHEME)
        # 4)Проверка того, что имеет ли электронная почта правильный домен.
        assert item['email'].endswith(EMAIL_ENDS)

    # 5)Проверка того, что ID,которое приходит в ответе, содержится в аватаре,в конце названия файла
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

#Мои методы
def test_list_resources():
    response = httpx.get(BASE_URL + LIST)
    # 1)Проверка,что код ответа равен 200
    assert response.status_code == 200
    data = response.json()['data']
    # 2)Проверка, что список не пустой
    assert len(data) > 0, "Список в ответе пустой"

    for item in data:
        validate(item, USER_DATA_SCHEME2)
        name = item.get('name')
        color = item.get('color')
        # 3)Проверка,значение поля не пустое
        assert name, "Field 'name' empty"
        assert color, "Field 'name' empty"
        # 4)Проверка наличия цвета в списке цветов. Получаем шестнадцатеричный код цвета в CSS4_COLORS по названию
        #Если name не найдено, то вернется None
        hex_color = mcolors.CSS4_COLORS.get(name)
        # 5)Проверка,что цвет с заданным именем действительно существует в словаре CSS4_COLORS
        # Если hex_color равен None, это означает, что цвет не был найден
        assert hex_color is not None, f"Color '{name}' not found in CSS4_COLORS"
        # 6)Проверка,что полученный цвет (hex_color) совпадает со значением переменной color
        assert hex_color == color, f"Field 'name' ('{name}') does not match field 'color' ('{color}')"

def test_single_resources():
    VALID_ID = 2
    response = httpx.get((BASE_URL+SINGLE_RESOURCES+f"{VALID_ID}"))

    # 1) Проверка, что код ответа равен 200
    assert response.status_code == 200

    # Получаем весь JSON-ответ
    json_data = response.json()

    # Подготовка для следующих проверок в методе
    data = json_data['data']
    support = json_data['support']

    # 2) Проверка, что в ответе, строка url содержит 'https://reqres.in'
    assert 'https://reqres.in' in support['url']

    # 3) Проверка, что в ответе, строка text не пустая
    assert len(support['text']) > 0, "Строка text пустая"

    # 4) Проверка, что возвращенные данные по ID корректны
    assert data['id'] == VALID_ID, f"Ожидали ID {VALID_ID}, но получили {data['id']}"
    assert 'name' in data, "Отсутствует name в данных"
    assert 'year' in data, "Отсутствует year в данных"
    assert 'color' in data, "Отсутствует color в данных"
    assert 'pantone_value' in data, "Отсутствует pantone_value в данных"

    # 5)Проверка,что в ответе, определенное поле содержит опреденное значение
    expected_name = "fuchsia rose"
    expected_year = "2001"
    expected_color = "#C74375"
    expected_pantone_value = "17-2031"

    assert data['name'] == expected_name, f"Ожидали name {expected_name}, но получили {data['name']}"
    assert data['year'] == int(expected_year), f"Ожидали year {expected_year}, но получили {data['year']}"
    assert data['color'] == expected_color, f"Ожидали color {expected_color}, но получили {data['color']}"
    assert data['pantone_value'] == expected_pantone_value, f"Ожидали pantone_value {expected_pantone_value}, но получили {data['pantone_value']}"

def test_single_resource_not_found():
    response = httpx.get(BASE_URL + NOT_FOUND_SINGLE_RESOURCES)
    # 1)Проверка,что код ответа - 404
    assert response.status_code == 404