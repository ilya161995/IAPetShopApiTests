import allure
import jsonschema
import requests
import pytest
from .schemas.store_schemas import STORE_SCHEMA

BASE_URL = "http://5.181.109.28:9090/api/v3"

@allure.feature("Store")
class TestStore:
    @allure.title("Размещение заказа")
    def test_add_order(self):
        with allure.step("Подготовка данных для размещение заказа"):
            payload = {
                "id": 1,
                "petId": 1,
                "quantity": 1,
                "status": "placed",
                "complete": True
            }
        with allure.step("Отправка запроса на размещение заказа"):
            response = requests.post(f"{BASE_URL}/store/order", json=payload)
            response_json = response.json()

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200

        with allure.step("Проверка параметров заказа в ответе"):
            assert response_json['id'] == payload['id'], "id не совпадает с ожидаемым"
            assert response_json['petId'] == payload['petId'], "petId не совпадает с ожидаемым"
            assert response_json['quantity'] == payload['quantity'], "quantity не совпадает с ожидаемым"
            assert response_json['status'] == payload['status'], "status  не совпадает с ожидаемым"
            assert response_json['complete'] == payload['complete'], "complete  не совпадает с ожидаемым"

    @allure.title("Получение информации о заказе по ID")
    def test_get_order_by_id(self):
        with allure.step("Отправка запроса на получение информации о заказе по ID"):
            response = requests.get(f"{BASE_URL}/store/order/1")

        with allure.step("Проверка статуса ответа и данных о заказе"):
            assert response.status_code == 200
            assert response.json()["id"] == 1

    @allure.title("Удаление заказа по ID")
    def test_delete_order_by_id(self):
        with allure.step("Отправка запроса на удаление заказа по ID"):
            response = requests.delete(f"{BASE_URL}/store/order/1")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200

        with allure.step("Отправка запроса на получение информации о заказе по ID"):
            response = requests.get(f"{BASE_URL}/store/order/1")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404

    @allure.title("Попытка получить информацию о несуществующем заказе")
    def test_get_information_nonexistent_order(self):
        with allure.step("Отправка запроса на получение информации о несуществующем заказе"):
            response = requests.get(url=f"{BASE_URL}/store/order/9999")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404

    @allure.title("Получение инвентаря магазина")
    def test_get_store_inventory(self):
        with allure.step("Отправка запроса на получение инвенторя"):
            response = requests.get(f"{BASE_URL}/store/inventory")

        with allure.step("Проверка статуса ответа и валидация JSON-схемы"):
            assert response.status_code == 200
            jsonschema.validate(response.json(), STORE_SCHEMA)