import httpx
from jsonschema import validate
from core.contracts import CREATE_USER_SCHEME
from core.contracts import UPDATE_USER_SCHEME
import datetime

BASE_URL = "https://reqres.in/"
CREATE_USER = "api/users"
PUT_USER = "api/users/2"

def test_create_user_with_name_and_job():
    body = {
        "name": "morpheus",
        "job": "leader"
    }
    response = httpx.post(BASE_URL + CREATE_USER, json=body)
    print(response.json())
    assert response.status_code == 201
    response_json = response.json()

    creation_date = response_json['createdAt'].replace('T', ' ')
    current_date = str(datetime.datetime.now(datetime.UTC))

    validate(response_json, CREATE_USER_SCHEME)
    assert (response_json['name'] == body['name'])
    assert (response_json['job'] == body['job'])
    assert creation_date[0:16] == current_date[0:16]


def test_create_user_without_name():
    body = {
        "job": "leader"
    }
    response = httpx.post(BASE_URL + CREATE_USER, json=body)
    print(response.json())
    assert response.status_code == 201
    response_json = response.json()

    creation_date = response_json['createdAt'].replace('T', ' ')
    current_date = str(datetime.datetime.now(datetime.UTC))

    validate(response_json, CREATE_USER_SCHEME)
    assert (response_json['job'] == body['job'])
    assert creation_date[0:16] == current_date[0:16]


def test_create_user_without_name():
    body = {
        "job": "leader"
    }
    response = httpx.post(BASE_URL + CREATE_USER, json=body)
    print(response.json())
    assert response.status_code == 201
    response_json = response.json()

    creation_date = response_json['createdAt'].replace('T', ' ')
    current_date = str(datetime.datetime.now(datetime.UTC))

    validate(response_json, CREATE_USER_SCHEME)
    assert (response_json['job'] == body['job'])
    assert creation_date[0:16] == current_date[0:16]

def test_create_user_without_job():
    body = {
        "name": "morpheus"
    }
    response = httpx.post(BASE_URL + CREATE_USER, json=body)
    print(response.json())
    assert response.status_code == 201
    response_json = response.json()

    creation_date = response_json['createdAt'].replace('T', ' ')
    current_date = str(datetime.datetime.now(datetime.UTC))

    validate(response_json, CREATE_USER_SCHEME)
    assert (response_json['name'] == body['name'])
    assert creation_date[0:16] == current_date[0:16]

def test_put_in_data_user():
    body = {
        "name": "morpheus",
        "job": "zion resident"
    }

    response = httpx.put(BASE_URL + PUT_USER, json=body)
    response_json = response.json()
    creation_date = response_json['updatedAt'].replace('T', ' ')
    current_date = str(datetime.datetime.now(datetime.UTC))

    assert response.status_code == 200
    validate(response_json, UPDATE_USER_SCHEME)
    assert 'name' in response_json
    assert 'job' in response_json
    assert creation_date[0:16] == current_date[0:16]

def test_put_in_data_user_without_name():
    body = {
        "job": "zion resident"
    }

    response = httpx.put(BASE_URL + PUT_USER, json=body)
    response_json = response.json()

    creation_date = response_json['updatedAt'].replace('T', ' ')
    current_date = str(datetime.datetime.now(datetime.UTC))

    assert response.status_code == 200
    validate(response_json, UPDATE_USER_SCHEME)
    assert 'job' in response_json
    assert 'name' not in response_json
    assert creation_date[0:16] == current_date[0:16]

def test_put_in_data_user_without_job():
    body = {
        "name": "morpheus"
    }

    response = httpx.put(BASE_URL + PUT_USER, json=body)
    print('Ваш ответ: ' + response.text)

    response_json = response.json()

    creation_date = response_json['updatedAt'].replace('T', ' ')
    current_date = str(datetime.datetime.now(datetime.UTC))

    assert response.status_code == 200
    validate(response_json, UPDATE_USER_SCHEME)
    assert 'job' not in response_json
    assert 'name' in response_json
    assert creation_date[0:16] == current_date[0:16]

def test_patch_in_data_user():
    body = {
        "name": "morpheus",
        "job": "zion resident"
    }

    response = httpx.patch(BASE_URL + PUT_USER, json=body)
    print('Ваш ответ: ' + response.text)

    response_json = response.json()

    creation_date = response_json['updatedAt'].replace('T', ' ')
    current_date = str(datetime.datetime.now(datetime.UTC))

    assert response.status_code == 200
    validate(response_json, UPDATE_USER_SCHEME)
    assert 'name' in response_json
    assert 'job' in response_json
    assert creation_date[0:16] == current_date[0:16]

def test_patch_in_data_user_without_name():
    body = {
        "job": "zion resident"
    }

    response = httpx.patch(BASE_URL + PUT_USER, json=body)
    print('Ваш ответ: ' + response.text)

    response_json = response.json()

    creation_date = response_json['updatedAt'].replace('T', ' ')
    current_date = str(datetime.datetime.now(datetime.UTC))

    assert response.status_code == 200
    validate(response_json, UPDATE_USER_SCHEME)
    assert 'job' in response_json
    assert 'name' not in response_json
    assert creation_date[0:16] == current_date[0:16]

def test_patch_in_data_user_without_job():
    body = {
        "name": "morpheus"
    }

    response = httpx.patch(BASE_URL + PUT_USER, json=body)
    print('Ваш ответ: ' + response.text)

    response_json = response.json()

    creation_date = response_json['updatedAt'].replace('T', ' ')
    current_date = str(datetime.datetime.now(datetime.UTC))

    assert response.status_code == 200
    validate(response_json, UPDATE_USER_SCHEME)
    assert 'name' in response_json
    assert 'job' not in response_json
    assert creation_date[0:16] == current_date[0:16]

def test_delete_user():
    response = httpx.delete(BASE_URL + PUT_USER)
    assert response.status_code == 204
