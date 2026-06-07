import pytest
import requests
import allure

from urls import ORDERS_URL
from data import OrderData


class TestCreateOrder:

    @allure.title('Создание заказа с разными цветами возвращает 201 и track')
    @pytest.mark.parametrize(
        "color",
        [
            ["BLACK"],
            ["GREY"],
            ["BLACK", "GREY"],
            []
        ]
    )
    def test_create_order_with_different_colors_returns_201_and_track(self, color):
        order_data = OrderData.order.copy()
        order_data["color"] = color

        response = requests.post(ORDERS_URL, json=order_data)

        assert response.status_code == 201
        assert "track" in response.json()