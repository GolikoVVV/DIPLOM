"""
UI-тесты с использованием мок-объектов 
для поискового сервиса https://www.kinopoisk.ru/
"""

import allure
import pytest
from unittest.mock import MagicMock
from selenium.webdriver.common.by import By


class KinopoiskPage:
    """
    Page Object класс для работы с главной страницей Кинопоиска
    Реализует основные элементы и действия на странице
    """
    def __init__(self, driver):
        """Инициализация с передачей драйвера"""
        self.driver = driver
    @allure.step("Получить поле поиска")
    def get_search_input(self):
        """Получение элемента поля поиска по имени 'kp_query'"""
        return self.driver.find_element(By.NAME, "kp_query")
    @allure.step("Получить логотип")
    def get_logo(self):
        """Получение элемента логотипа по классу 'header-logo'"""
        return self.driver.find_element(By.CLASS_NAME, "header-logo")
    @allure.step("Выполнить поиск: {query}")
    def search(self, query):
        """
        Выполнение поискового запроса
        Args:
            query (str): Поисковый запрос
        """
        search_input = self.get_search_input()
        search_input.clear()  # Очищаем поле перед вводом
        search_input.send_keys(query)  # Вводим поисковый запрос
        search_input.submit()  # Отправляем форму поиска
    @allure.step("Кликнуть по логотипу")
    def click_logo(self):
        """Клик по логотипу для возврата на главную страницу"""
        self.get_logo().click()


@pytest.fixture
def mock_driver():
    """
    Фикстура для создания мок-объекта WebDriver
    Заменяет реальный браузер для изолированного тестирования
    """
    driver = MagicMock()
    element = MagicMock()
    # Настраиваем поведение мок-элемента
    element.is_displayed.return_value = True  # Элемент всегда видим
    element.is_enabled.return_value = True    # Элемент всегда доступен
    # Настраиваем поведение мок-драйвера
    # Все find_element возвращают наш элемент
    driver.find_element.return_value = element
    # Множественные элементы
    driver.find_elements.return_value = [element, element, element]
    driver.title = "КиноПоиск"  # Заголовок страницы
    driver.current_url = "https://www.kinopoisk.ru/"  # URL страницы
    return driver


@allure.epic("UI Тесты Кинопоиска")
@allure.feature("Базовые тесты с моками")
class TestSimpleKinopoisk:
    """Тестовый класс для проверки базовой функциональности Кинопоиска"""
    @allure.story("Загрузка страницы")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.description("Проверяем корректность загрузки главной страницы")
    def test_1_page_loading(self, mock_driver):
        """Тест 1: Проверка корректной загрузки страницы"""
        page = KinopoiskPage(mock_driver)
        
        with allure.step("Проверка заголовка"):
            # Проверяем, что заголовок содержит ожидаемое значение
            assert "КиноПоиск" in page.driver.title
            # Прикрепляем информацию о заголовке в отчет
            allure.attach(f"Заголовок: {page.driver.title}", name="page_title")
        
        with allure.step("Проверка URL"):
            # Проверяем корректность URL адреса
            assert "kinopoisk.ru" in page.driver.current_url
            # Прикрепляем информацию о URL в отчет
            allure.attach(f"URL: {page.driver.current_url}", name="page_url")
    
    @allure.story("Элементы интерфейса") 
    @allure.severity(allure.severity_level.CRITICAL)
    def test_2_ui_elements(self, mock_driver):
        """Тест 2: Проверка наличия и доступности основных UI элементов"""
        page = KinopoiskPage(mock_driver)
        
        with allure.step("Проверка поля поиска"):
            # Получаем элемент поля поиска
            search_input = page.get_search_input()
            # Проверяем, что поле отображается и доступно
            assert search_input.is_displayed()
            assert search_input.is_enabled()
            allure.attach("Поле поиска доступно", name="search_input_ok")
        
        with allure.step("Проверка логотипа"):
            # Получаем элемент логотипа
            logo = page.get_logo()
            # Проверяем, что логотип отображается
            assert logo.is_displayed()
            allure.attach("Логотип отображается", name="logo_ok")
    
    @allure.story("Функциональность поиска")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_3_search_functionality(self, mock_driver):
        """Тест 3: Проверка функциональности поиска"""
        page = KinopoiskPage(mock_driver)
        
        test_query = "Интерстеллар"
        with allure.step(f"Выполнение поиска: {test_query}"):
            # Выполняем поиск с тестовым запросом
            page.search(test_query)
        
        with allure.step("Проверка вызовов методов"):
            # Получаем элемент для проверки вызовов методов
            search_input = page.get_search_input()
            
            # Проверяем, что все методы были вызваны корректно
            search_input.clear.assert_called_once()  # Очистка вызвана 1 раз
            search_input.send_keys.assert_called_with(test_query)  # Ввод правильного запроса
            search_input.submit.assert_called_once()  # Отправка вызвана 1 раз
            
            # Формируем детальную информацию о вызовах для отчета
            calls_info = f"""
            Проверенные вызовы:
            - clear: ✓
            - send_keys: ✓ ({test_query})
            - submit: ✓
            """
            allure.attach(calls_info, name="method_calls_verified")
    
    @allure.story("Навигация")
    @allure.severity(allure.severity_level.NORMAL)
    def test_4_navigation(self, mock_driver):
        """Тест 4: Проверка навигации по сайту"""
        page = KinopoiskPage(mock_driver)
        
        with allure.step("Клик по логотипу"):
            # Выполняем клик по логотипу
            page.click_logo()
        
        with allure.step("Проверка клика"):
            # Проверяем, что метод click был вызван
            page.get_logo().click.assert_called_once()
            allure.attach("Клик по логотипу подтвержден", name="logo_click_confirmed")
    
    @allure.story("Ввод данных")
    @allure.severity(allure.severity_level.NORMAL)
    def test_5_input_validation(self, mock_driver):
        """Тест 5: Проверка ввода и валидации данных"""
        page = KinopoiskPage(mock_driver)
        search_input = page.get_search_input()
        
        with allure.step("Тест ввода текста"):
            # Проверяем ввод текста в поле поиска
            search_input.send_keys("test")
            search_input.send_keys.assert_called_with("test")
            allure.attach("Ввод текста проверен", name="text_input_ok")
        
        with allure.step("Тест очистки поля"):
            # Проверяем очистку поля ввода
            search_input.clear()
            search_input.clear.assert_called()
            allure.attach("Очистка поля проверена", name="clear_ok")


if __name__ == "__main__":
    """
    Точка входа для прямого запуска тестов
    Генерирует Allure отчеты в директорию allure-results
    """
    # Запуск тестов с настройками для Allure
    pytest.main([
        __file__, 
        "-v",                    # Подробный вывод
        "-s",                    # Вывод print-ов
        "--alluredir=allure-results",  # Директория для результатов Allure
        "--clean-alluredir"      # Очистка предыдущих результатов
    ])