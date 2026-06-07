import requests
import allure

from urls import ORDERS_URL


class TestGetOrders:

    @allure.title('Получение списка заказов возвращает 200 и список orders')
    def test_get_orders_returns_200_and_orders_list(self):
        response = requests.get(ORDERS_URL, params={"limit": 10})

        assert response.status_code == 200
        assert "orders" in response.json()
        assert isinstance(response.json()["orders"], list)