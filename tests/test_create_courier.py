import pytest
import requests
import allure

from urls import CREATE_COURIER_URL
from data import CourierData, ResponseText
from helpers import generate_courier_data, delete_courier


class TestCreateCourier:

    @allure.title('Создание курьера с валидными данными возвращает 201 и ok true')
    def test_create_courier_valid_data_returns_201_and_ok_true(self):
        courier_data = generate_courier_data()

        response = requests.post(CREATE_COURIER_URL, json=courier_data)

        assert response.status_code == 201
        assert response.json()["ok"] is True

        delete_courier(courier_data["login"], courier_data["password"])

    @allure.title('Создание двух одинаковых курьеров возвращает ошибку')
    def test_create_two_same_couriers_returns_409_and_error_message(self):
        courier_data = generate_courier_data()

        requests.post(CREATE_COURIER_URL, json=courier_data)
        response = requests.post(CREATE_COURIER_URL, json=courier_data)

        assert response.status_code == 409
        assert response.json()["message"] == ResponseText.CREATE_COURIER_DUPLICATE_LOGIN

        delete_courier(courier_data["login"], courier_data["password"])

    @allure.title('Создание курьера без обязательного поля возвращает ошибку')
    @pytest.mark.parametrize(
        "courier_data",
        [
            CourierData.courier_without_login,
            CourierData.courier_without_password
        ]
    )
    def test_create_courier_without_required_field_returns_400_and_error_message(self, courier_data):
        response = requests.post(CREATE_COURIER_URL, json=courier_data)

        assert response.status_code == 400
        assert response.json()["message"] == ResponseText.CREATE_COURIER_NOT_ENOUGH_DATA