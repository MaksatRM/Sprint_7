import random
import string
import requests

from urls import CREATE_COURIER_URL, LOGIN_COURIER_URL


def generate_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))


def generate_courier_data():
    return {
        "login": generate_random_string(10),
        "password": generate_random_string(10),
        "firstName": generate_random_string(10)
    }


def register_new_courier_and_return_login_password():
    login_pass = []

    courier_data = generate_courier_data()

    response = requests.post(CREATE_COURIER_URL, json=courier_data)

    if response.status_code == 201:
        login_pass.append(courier_data["login"])
        login_pass.append(courier_data["password"])
        login_pass.append(courier_data["firstName"])

    return login_pass


def delete_courier(login, password):
    login_response = requests.post(LOGIN_COURIER_URL, json={
        "login": login,
        "password": password
    })

    if login_response.status_code == 200:
        courier_id = login_response.json()["id"]
        requests.delete(f'{CREATE_COURIER_URL}/{courier_id}')