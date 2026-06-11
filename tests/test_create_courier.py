import pytest
import requests
import allure

from urls import CREATE_COURIER_URL
from data import CourierData, ResponseText
from helpers import generate_courier_data, delete_courier


@pytest.fixture
def generated_courier_data():
    courier_data = generate_courier_data()
    yield courier_data

    with allure.step('Удалить созданного курьера'):
        delete_courier(courier_data["login"], courier_data["password"])


class TestCreateCourier:

    @allure.title('Создание курьера с валидными данными возвращает 201 и ok true')
    def test_create_courier_valid_data_returns_201_and_ok_true(self, generated_courier_data):
        with allure.step('Отправить запрос на создание курьера с валидными данными'):
            response = requests.post(CREATE_COURIER_URL, json=generated_courier_data)

        with allure.step('Проверить код ответа и тело ответа'):
            assert response.status_code == 201
            assert response.json()["ok"] is True

    @allure.title('Создание двух одинаковых курьеров возвращает ошибку')
    def test_create_two_same_couriers_returns_409_and_error_message(self, generated_courier_data):
        with allure.step('Создать первого курьера'):
            requests.post(CREATE_COURIER_URL, json=generated_courier_data)

        with allure.step('Отправить повторный запрос на создание курьера с тем же логином'):
            response = requests.post(CREATE_COURIER_URL, json=generated_courier_data)

        with allure.step('Проверить код ответа и сообщение об ошибке'):
            assert response.status_code == 409
            assert response.json()["message"] == ResponseText.CREATE_COURIER_DUPLICATE_LOGIN

    @allure.title('Создание курьера без обязательного поля возвращает ошибку')
    @pytest.mark.parametrize(
        "courier_data",
        [
            CourierData.courier_without_login,
            CourierData.courier_without_password
        ]
    )
    def test_create_courier_without_required_field_returns_400_and_error_message(self, courier_data):
        with allure.step('Отправить запрос на создание курьера без обязательного поля'):
            response = requests.post(CREATE_COURIER_URL, json=courier_data)

        with allure.step('Проверить код ответа и сообщение об ошибке'):
            assert response.status_code == 400
            assert response.json()["message"] == ResponseText.CREATE_COURIER_NOT_ENOUGH_DATA