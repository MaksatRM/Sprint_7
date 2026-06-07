import pytest
import requests
import allure

from urls import LOGIN_COURIER_URL
from data import LoginData, LoginResponseText
from helpers import register_new_courier_and_return_login_password, delete_courier


class TestLoginCourier:

    @allure.title('Логин курьера с валидными данными возвращает 200 и id')
    def test_login_courier_valid_data_returns_200_and_id(self):
        login_pass = register_new_courier_and_return_login_password()

        login_data = {
            "login": login_pass[0],
            "password": login_pass[1]
        }

        response = requests.post(LOGIN_COURIER_URL, json=login_data)

        assert response.status_code == 200
        assert "id" in response.json()

        delete_courier(login_pass[0], login_pass[1])

    @allure.title('Логин курьера без обязательного поля возвращает ошибку')
    @pytest.mark.parametrize(
        "login_data",
        [
            LoginData.courier_without_login,
            LoginData.courier_without_password
        ]
    )
    def test_login_courier_without_required_field_returns_400_and_error_message(self, login_data):
        response = requests.post(LOGIN_COURIER_URL, json=login_data)

        assert response.status_code == 400
        assert response.json()["message"] == LoginResponseText.LOGIN_NOT_ENOUGH_DATA

    @allure.title('Логин несуществующего курьера возвращает ошибку')
    def test_login_nonexistent_courier_returns_404_and_error_message(self):
        response = requests.post(LOGIN_COURIER_URL, json=LoginData.nonexistent_courier)

        assert response.status_code == 404
        assert response.json()["message"] == LoginResponseText.LOGIN_ACCOUNT_NOT_FOUND

    @allure.title('Логин курьера с неправильным паролем возвращает ошибку')
    def test_login_courier_wrong_password_returns_404_and_error_message(self):
        login_pass = register_new_courier_and_return_login_password()

        login_data = {
            "login": login_pass[0],
            "password": "wrong_password"
        }

        response = requests.post(LOGIN_COURIER_URL, json=login_data)

        assert response.status_code == 404
        assert response.json()["message"] == LoginResponseText.LOGIN_ACCOUNT_NOT_FOUND

        delete_courier(login_pass[0], login_pass[1])