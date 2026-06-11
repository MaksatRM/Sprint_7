import pytest
import requests
import allure

from urls import LOGIN_COURIER_URL
from data import LoginData, LoginResponseText
from helpers import register_new_courier_and_return_login_password, delete_courier


@pytest.fixture
def created_courier():
    login_pass = register_new_courier_and_return_login_password()
    yield login_pass

    with allure.step('Удалить созданного курьера'):
        delete_courier(login_pass[0], login_pass[1])


class TestLoginCourier:

    @allure.title('Логин курьера с валидными данными возвращает 200 и id')
    def test_login_courier_valid_data_returns_200_and_id(self, created_courier):
        login_data = {
            "login": created_courier[0],
            "password": created_courier[1]
        }

        with allure.step('Отправить запрос на логин курьера с валидными данными'):
            response = requests.post(LOGIN_COURIER_URL, json=login_data)

        with allure.step('Проверить код ответа и наличие id в теле ответа'):
            assert response.status_code == 200
            assert "id" in response.json()

    @allure.title('Логин курьера без обязательного поля возвращает ошибку')
    @pytest.mark.parametrize(
        "login_data",
        [
            LoginData.courier_without_login,
            LoginData.courier_without_password
        ]
    )
    def test_login_courier_without_required_field_returns_400_and_error_message(self, login_data):
        with allure.step('Отправить запрос на логин курьера без обязательного поля'):
            response = requests.post(LOGIN_COURIER_URL, json=login_data)

        with allure.step('Проверить код ответа и сообщение об ошибке'):
            assert response.status_code == 400
            assert response.json()["message"] == LoginResponseText.LOGIN_NOT_ENOUGH_DATA

    @allure.title('Логин несуществующего курьера возвращает 404 и сообщение об ошибке')
    def test_login_nonexistent_courier_returns_404_and_error_message(self):
        with allure.step('Отправить запрос на логин несуществующего курьера'):
            response = requests.post(LOGIN_COURIER_URL, json=LoginData.nonexistent_courier)

        with allure.step('Проверить код ответа и сообщение об ошибке'):
            assert response.status_code == 404
            assert response.json()["message"] == LoginResponseText.LOGIN_ACCOUNT_NOT_FOUND

    @allure.title('Логин курьера с неправильным паролем возвращает 404 и сообщение об ошибке')
    def test_login_courier_wrong_password_returns_404_and_error_message(self, created_courier):
        login_data = {
            "login": created_courier[0],
            "password": "wrong_password"
        }

        with allure.step('Отправить запрос на логин курьера с неправильным паролем'):
            response = requests.post(LOGIN_COURIER_URL, json=login_data)

        with allure.step('Проверить код ответа и сообщение об ошибке'):
            assert response.status_code == 404
            assert response.json()["message"] == LoginResponseText.LOGIN_ACCOUNT_NOT_FOUND