class CourierData:
    courier_without_login = {
        "password": "123456",
        "firstName": "Maksat"
    }

    courier_without_password = {
        "login": "maksat_test_login",
        "firstName": "Maksat"
    }


class ResponseText:
    CREATE_COURIER_NOT_ENOUGH_DATA = "Недостаточно данных для создания учетной записи"
    CREATE_COURIER_DUPLICATE_LOGIN = "Этот логин уже используется. Попробуйте другой."
    
class LoginData:
    courier_without_login = {
        "password": "123456"
    }

    courier_without_password = {
        "login": "maksat_test_login"
    }

    nonexistent_courier = {
        "login": "nonexistent_login",
        "password": "123456"
    }


class LoginResponseText:
    LOGIN_NOT_ENOUGH_DATA = "Недостаточно данных для входа"
    LOGIN_ACCOUNT_NOT_FOUND = "Учетная запись не найдена"

class OrderData:
    order = {
        "firstName": "Naruto",
        "lastName": "Uchiha",
        "address": "Konoha, 142 apt.",
        "metroStation": 4,
        "phone": "+7 800 355 35 35",
        "rentTime": 5,
        "deliveryDate": "2026-06-08",
        "comment": "Saske, come back to Konoha"
    }