"""
API-тесты для поискового сервиса https://www.kinopoisk.ru/
Тесты проверяют различные сценарии работы поискового API
"""

import allure
from data import TestData
from base_api import BaseAPI


class TestAPI:
    """Класс тестов для API поискового сервиса"""
    @allure.feature("API Tests")
    @allure.story("Поиск по кириллице")
    def test_search_cyrillic(self):
        """Тест поиска с кириллическим запросом"""
        # Создаем экземпляр API клиента
        api = BaseAPI()
        with allure.step("Выполнение поиска"):
            # Отправляем поисковый запрос с кириллическим текстом
            response = api.search(TestData.SEARCH_CYRILLIC)
        with allure.step("Проверка статуса ответа"):
            # Проверяем, что API вернул успешный статус 200
            assert response.status_code == 200
        with allure.step("Проверка наличия результата"):
            # Проверяем, что ответ содержит искомый кириллический текст
            assert TestData.SEARCH_CYRILLIC in response.text

    @allure.story("Поиск по латинице")
    def test_search_latin(self):
        """Тест поиска с латинским запросом"""
        api = BaseAPI()
        with allure.step("Выполнение поиска"):
            # Отправляем поисковый запрос с латинским текстом
            response = api.search(TestData.SEARCH_LATIN)
        with allure.step("Проверка статуса ответа"):
            # Проверяем успешный статус ответа
            assert response.status_code == 200
        with allure.step("Проверка наличия результата"):
            # Проверяем наличие латинского текста в ответе
            assert TestData.SEARCH_LATIN in response.text

    @allure.story("Поиск по спецсимволам")
    def test_search_special(self):
        """Тест поиска с запросом содержащим специальные символы"""
        api = BaseAPI()
        with allure.step("Выполнение поиска"):
            # Отправляем запрос со специальными символами
            response = api.search(TestData.SEARCH_SPECIAL)
        with allure.step("Проверка статуса ответа"):
            # Проверяем, что API корректно обработал запрос со спецсимволами
            assert response.status_code == 200

    @allure.story("Поиск без API ключа")
    def test_no_api_key(self):
        """Тест авторизации - запрос без API ключа"""
        api = BaseAPI()
        # Убираем API ключ из заголовков для проверки авторизации
        api.headers = {'Content-Type': 'application/json'}  # Убираем ключ
        with allure.step("Выполнение запроса без ключа"):
            # Пытаемся выполнить запрос без авторизации
            response = api.search("Matrix")
        with allure.step("Проверка статуса ответа"):
            # Ожидаем ошибку авторизации 401 (Unauthorized)
            assert response.status_code == 401

    @allure.story("Поиск пустого запроса")
    def test_search_empty(self):
        """Тест обработки пустого поискового запроса"""
        api = BaseAPI()
        with allure.step("Выполнение поиска пустого запроса"):
            # Отправляем пустой запрос для проверки обработки edge case
            response = api.search(TestData.SEARCH_EMPTY)
        with allure.step("Проверка статуса ответа"):
            # Проверяем, что API корректно обрабатывает пустые запросы
            assert response.status_code == 200

    @allure.story("Поиск с невалидным API ключом")
    def test_invalid_api_key(self):
        """Тест авторизации с невалидным API ключом"""
        api = BaseAPI()
        # Устанавливаем заведомо неверный API ключ
        api.headers['X-API-KEY'] = 'BAD-KEY'  # Создаем невалидный ключ
        with allure.step("Выполнение запроса с невалидным ключом"):
            # Пытаемся выполнить запрос с некорректным ключом авторизации
            response = api.search("Matrix")
        with allure.step("Проверка статуса ответа"):
            # Ожидаем ошибку авторизации 401
            assert response.status_code == 401
