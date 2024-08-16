from selenium.webdriver.common.by import By
from ruts_auto_ui.tests_ui.pages.base import Base
import allure
from abc import ABC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.action_chains import ActionChains


class MessageForm(Base, ABC):
    BUTTON: tuple
    CHECKBOX: tuple
    FORM_NAME: str
    LINK: list
    SUCCESS_MESSAGE: tuple
    TEXT_BUTTON: str
    TEXT_MESSAGE: str

    def button_is_desabled(self) -> None:
        with allure.step(f"Проверить, что кнопка '{self.TEXT_BUTTON}' неактивна"):
            self.must_be_active(self.BUTTON, "NO")

    def push_button(self) -> None:
        with allure.step(f"Нажать на кнопку '{self.TEXT_BUTTON}'"):
            self.browser.find_element(*self.BUTTON).click()

    @allure.step("Отметить чекбокс")
    def tick_checkbox(self) -> None:
        checkbox = self.browser.find_element(*self.CHECKBOX)
        action = ActionChains(self.browser)
        action.move_to_element(checkbox).perform()
        action.click(checkbox).perform()
        self.browser.find_element(*self.CHECKBOX).is_selected()

    def has_success_message(self, txt=None) -> None:
        if txt is None:
            txt = self.TEXT_MESSAGE
        with allure.step(f"Проверить, что появилось сообщение '{txt}'"):
            WebDriverWait(self.browser, 3).until(ec.visibility_of_all_elements_located(self.SUCCESS_MESSAGE))
            self.has_text(self.SUCCESS_MESSAGE, txt)


class Field(Base):
    FIELD_CASH = {}

    def enter_field(self, locator: tuple, text: str or float or int, descr: str = "",
                    limit: int or None = None) -> None:
        var = text if (limit == None or len(text) < limit) else f'символы ({len(text)} шт.)'
        with allure.step(f"Ввести '{var}' в поле '{descr}'"):
            self.enter_data(locator, text)
        self.FIELD_CASH.update({descr: text})

    def clear_field(self, locator, descr="") -> None:
        with allure.step(f"Очистить поле '{descr}'"):
            self.browser.find_element(*locator).clear()
        self.FIELD_CASH.update({descr: ""})

    def has_error(self, locator: tuple, text: str, field_errors: dict, default_message: str, obligatory=True) -> None:
        error_message = None
        if text is "" and obligatory:
            error_message = "Обязательное поле"
        else:
            for key in field_errors:
                if key(text) is True:
                    error_message = field_errors[key]
            if error_message is None:
                error_message = default_message

        with allure.step(f"Проверить, что возникла ошибка с сообщением: '{error_message}'"):
            WebDriverWait(self.browser, 3).until(ec.visibility_of_all_elements_located(locator))
            self.has_text(locator, error_message)


class EmailField(Field):
    DEFAULT_EMAIL_ERROR = "Введите действительный email в формате name@example.com"
    LIMIT_DOMAIN = None
    MAX_DOMAIN = 63
    MAX_EMAIL = 256
    MIN_EMAIL = 7

    def requirement_email_errors(self) -> dict:
        return {
            lambda x: len(x) < self.MIN_EMAIL and x != "":
                f"Минимальная длина email - {self.MIN_EMAIL} символов",
            lambda x: len(x) > self.MAX_EMAIL:
                f"Максимальная длина email - {self.MAX_EMAIL} символов",
            lambda x: len(str(x).split("@")[
                              1]) > EmailField.MAX_DOMAIN if "@" in x else False:
                f"Максимальная длина домена - {self.LIMIT_DOMAIN} символа"
        }

    def is_email_error(self, email: str, locator: tuple, obligatory: bool = True):
        self.has_error(locator, email, self.requirement_email_errors(), self.DEFAULT_EMAIL_ERROR, obligatory=obligatory)


class FioField(Field):
    DEFAULT_FIO_ERROR = "Введите ФИО в формате Иванов Иван Иванович"
    MAX_FIO = 50

    def requirement_fio_errors(self) -> dict:
        return {
            lambda x: len(x) > self.MAX_FIO: f"Максимальная длина фио - {self.MAX_FIO} символов",
        }

    def is_fio_error(self, fio: str, locator: tuple, obligatory: bool = True):
        self.has_error(locator, fio, self.requirement_fio_errors(), self.DEFAULT_FIO_ERROR, obligatory=obligatory)


class MessageField(Field):
    DEFAULT_MESSAGE_ERROR = "Поле может содержать только символы латиницы и кириллицы, цифры пробел и дефис"
    MAX_MESSAGE = 500
    MIN_MESSAGE = 2

    def requirement_message_errors(self) -> dict:
        return {
            lambda x: len(x) > self.MAX_MESSAGE: f"Максимальная длина поля - {self.MAX_MESSAGE} символов",
            lambda x: len(x) < self.MIN_MESSAGE: f"Минимальная длина поля - {self.MIN_MESSAGE} символа"
        }

    def is_message_error(self, message: str or int or float, locator: tuple, obligatory: bool = True):
        self.has_error(locator, message, self.requirement_message_errors(), self.DEFAULT_MESSAGE_ERROR,
                       obligatory=obligatory)


class QueryForm(MessageForm, FioField, EmailField, MessageField):
    BUTTON = (By.CSS_SELECTOR, "#qa [type='submit']")
    CHECKBOX = (By.CSS_SELECTOR, "#qa .ant-checkbox-input")
    ERROR_EMAIL = (By.CSS_SELECTOR, "#qa #email_help")
    ERROR_FIO = (By.CSS_SELECTOR, "#qa #fio_help")
    ERROR_TEXT = (By.CSS_SELECTOR, "#qa #message_help")
    FIELD_EMAIL = (By.CSS_SELECTOR, "#qa #email")
    FIELD_FIO = (By.CSS_SELECTOR, "#qa #fio")
    FIELD_TEXT = (By.CSS_SELECTOR, "#qa #message")
    FORM_NAME = 'Задай вопрос'
    HELPER_EMAIL = "Ваш Email"
    HELPER_FIO = "ФИО"
    HELPER_TEXT = "Задайте вопрос"
    LINK = [Base.BASE_URL]
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, ".ant-notification-notice-message")
    TEXT_BUTTON = "Отправить"
    TEXT_MESSAGE = "Спасибо, ваша заявка принята!"

    def enter_fields(self,
                     fio,
                     email,
                     query) -> None:
        self.enter_field(self.FIELD_FIO, fio, self.HELPER_FIO)
        self.enter_field(self.FIELD_EMAIL, email, self.HELPER_EMAIL, self.MAX_EMAIL)
        self.enter_field(self.FIELD_TEXT, query, self.HELPER_TEXT, self.MAX_MESSAGE)

    def approve_error(self, field: str):
        type_fields = {
            self.HELPER_FIO: lambda text: self.is_fio_error(text, self.ERROR_FIO),
            self.HELPER_EMAIL: lambda text: self.is_email_error(text, self.ERROR_EMAIL),
            self.HELPER_TEXT: lambda text: self.is_message_error(text, self.ERROR_TEXT)
        }
        self.group_checker(field, "HELPER")
        type_fields[field](self.FIELD_CASH[field])


class CityForm(QueryForm):
    AUTO_LINK = {"cities": ["href", (By.CSS_SELECTOR, ".group .link")]
                 }
    BUTTON = (By.CSS_SELECTOR, ".bg-white [type='submit']")
    CHECKBOX = (By.CSS_SELECTOR, ".bg-white .ant-checkbox-input")
    ERROR_EMAIL = (By.CSS_SELECTOR, ".bg-white #email_help")
    ERROR_FIO = (By.CSS_SELECTOR, ".bg-white #fio_help")
    ERROR_TEXT = (By.CSS_SELECTOR, ".bg-white #message_help")
    FIELD_EMAIL = (By.CSS_SELECTOR, ".bg-white #email")
    FIELD_FIO = (By.CSS_SELECTOR, ".bg-white #fio")
    FIELD_TEXT = (By.CSS_SELECTOR, ".bg-white #message")
    FORM_NAME = 'Отправляй заявку'
    HELPER_EMAIL = "Ваш Email"
    HELPER_FIO = "ФИО"
    HELPER_TEXT = "Желаемый город"
    LINK = [Base.BASE_URL, Base.BASE_URL + "cities"]
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, ".ant-notification-notice-info")
    TEXT_BUTTON = "Отправить"
