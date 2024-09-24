import httpx
from jsonschema import validate
import matplotlib.colors as mcolors
from core.contracts import USER_DATA_SCHEME
from core.contracts3 import USER_DATA_SCHEME3
import allure

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
@allure.suite('Проверка запросов данных пользователей')
@allure.title("Проверка сценария получения списка пользователей")
def test_list_users():
    with allure.step(f'Делаем запрос по адресу: {BASE_URL + LIST_USERS}'):
        response = httpx.get(BASE_URL + LIST_USERS)
    with allure.step('Проверяем код ответа'):
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
        with allure.step('Проверяем окончание Email адрееса'):
            validate(item, USER_DATA_SCHEME)
        # 4)Проверка того, что имеет ли электронная почта правильный домен.
        with allure.step('Проверяем наличие id в ссылке на аватарку'):
            assert item['email'].endswith(EMAIL_ENDS)

    # 5)Проверка того, что ID,которое приходит в ответе, содержится в аватаре,в конце названия файла
    with allure.step('Проверяем,что ID в ответе,содержится в конце ссылки на аватарку'):
        assert item['avatar'].endswith(str(item['id']) + AVATAR_ENDS)


# Пишем проверки на метод SINGLE USER сайта https://reqres.in
@allure.suite('Проверка запросов данных пользователей')
@allure.title("Проверка сценария получения даннных пользователя")
def test_single_user():
    with allure.step(f'Делаем запрос по адресу: {BASE_URL + SINGLE_USER}'):
        response = httpx.get(BASE_URL + SINGLE_USER)
    with allure.step('Проверяем код ответа'):
        assert response.status_code == 200
    # Подготовка для слудующих проверок в методе
    data = response.json()['data']
    # print(response.json()['support'])
    with allure.step('Проверяем наличие id в ссылке на аватарку'):
        assert data['email'].endswith(EMAIL_ENDS)
    with allure.step('Проверяем,что ID в ответе,содержится в конце ссылки на аватарку'):
        assert data['avatar'].endswith(str(data['id']) + AVATAR_ENDS)


# Пишем проверки на метод SINGLE USER NOT FOUND сайта https://reqres.in
@allure.suite('Проверка запросов данных пользователей')
@allure.title("Проверка сценария, когда пользователь не найден в системе")
def test_user_not_found():
    with allure.step(f'Делаем запрос по адресу: {BASE_URL + NOT_FOUND_USER}'):
        response = httpx.get(BASE_URL + NOT_FOUND_USER)
    with allure.step('Проверяем код ответа'):
        assert response.status_code == 404


# Мои методы
@allure.suite('Проверка запросов данных пользователей')
@allure.title("Проверка сценария получения списка ресурсов в системе")
def test_list_resources():
    # Проверка-1
    with allure.step(f'Делаем запрос по адресу: {BASE_URL + LIST}'):
        response = httpx.get(BASE_URL + LIST)
    # Проверка-2
    with allure.step('Проверяем,что код ответа равен 200'):
        assert response.status_code == 200
    data = response.json()['data']
    # Проверка-3
    with allure.step('Проверяем,что список в ответе сервера не пустой'):
        assert len(data) > 0, "Список в ответе пустой"

    for item in data:
        with allure.step('Проверяем схему с заданным в contract3 шаблоном'):
            validate(item, USER_DATA_SCHEME3)
            name = item.get('name')
            color = item.get('color')
            # Проверка-4
            with allure.step('Проверяем,что значение поля name не пустое'):
                assert name, "Field 'name' empty"
            # Проверка-5
            with allure.step('Проверяем,что значение поля name не пустое'):
                assert color, "Field 'name' empty"


@allure.suite('Проверка запросов данных пользователей')
@allure.title("Проверка сценария получения ресурса в системе")
def test_single_resources():
    # Проверка-1
    VALID_ID = 2
    with allure.step(f'Делаем запрос по адресу: {BASE_URL + SINGLE_RESOURCES + str(VALID_ID)}'):
        response = httpx.get((BASE_URL + SINGLE_RESOURCES + f'{VALID_ID}'))
    # Проверка-2
    with allure.step('Проверяем,что код ответа равен 200'):
        assert response.status_code == 200

    # Получаем весь JSON-ответ
    json_data = response.json()

    # Подготовка для следующих проверок в методе
    data = json_data['data']
    support = json_data['support']

    # Проверка-2
    VERIFIED_VALUE = 'https://reqres.in'
    with allure.step(f'Проверяем,что в ответе,строка url содержит значение: {VERIFIED_VALUE}'):
        assert VERIFIED_VALUE in support['url']

    # Проверка-3
    with allure.step('Проверяем,что значение поля text в support не пустое'):
        assert len(support['text']) > 0, "Строка text пустая"

    # Проверка-4
    with allure.step(f'Проверяем,что ожидаемое id:{VALID_ID} равно фактическому'):
        assert data['id'] == VALID_ID, f"Ожидали ID {VALID_ID}, но получили {data['id']}"
    with allure.step('Проверяем наличие поля name в data'):
        assert 'name' in data, "Отсутствует name в данных"
    with allure.step('Проверяем наличие поля year в data'):
        assert 'year' in data, "Отсутствует year в данных"
    with allure.step('Проверяем наличие поля color в data'):
        assert 'color' in data, "Отсутствует color в данных"
    with allure.step('Проверяем наличие поля pantone_value в data'):
        assert 'pantone_value' in data, "Отсутствует pantone_value в данных"

    # Проверка-5
    expected_name = "fuchsia rose"
    expected_year = "2001"
    expected_color = "#C74375"
    expected_pantone_value = "17-2031"
    with allure.step(f'Проверяем, что ожидаемое значение поля name: {expected_name} равно фактическому'):
        assert data['name'] == expected_name, f"Ожидали name {expected_name}, но получили {data['name']}"
    with allure.step(f'Проверяем, что ожидаемое значение поля year: {expected_year} равно фактическому'):
        assert data['year'] == int(expected_year), f"Ожидали year {expected_year}, но получили {data['year']}"
    with allure.step(f'Проверяем, что ожидаемое значение поля color: {expected_color} равно фактическому'):
        assert data['color'] == expected_color, f"Ожидали color {expected_color}, но получили {data['color']}"
    with allure.step(
            f'Проверяем, что ожидаемое значение поля pantone_value: {expected_pantone_value} равно фактическому'):
        assert data[
                   'pantone_value'] == expected_pantone_value, f"Ожидали pantone_value {expected_pantone_value}, но получили {data['pantone_value']}"

    @allure.suite('Проверка запросов данных пользователей')
    @allure.title("Проверка сценария, когда ресурс не найден в системе")
    def test_single_resource_not_found():
        with allure.step(f'Делаем запрос по адресу: {BASE_URL + NOT_FOUND_SINGLE_RESOURCES}'):
            response = httpx.get(BASE_URL + NOT_FOUND_SINGLE_RESOURCES)
        # Проверка-1
        with allure.step('Проверяем,что код ответа равен 404'):
            assert response.status_code == 404
