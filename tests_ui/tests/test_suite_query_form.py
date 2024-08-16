import pytest
import allure
from allpairspy import AllPairs as Pairwise
from ruts_auto_ui.tests_ui.pages.message_form import QueryForm, CityForm
from ruts_auto_ui.utils.jsonreader import data
from ruts_auto_ui.utils.link_parser import link_parser

FIO, EMAIL, QUERY = data("fio", "email", "message")
LINKS = link_parser(QueryForm, CityForm)


@pytest.mark.usefixtures("setup")
@pytest.mark.parametrize("form_type, link", LINKS)
class TestQueryForm:

    @pytest.mark.parametrize("name, email, query",
                             Pairwise([
                                 FIO["valid"],
                                 EMAIL["valid"],
                                 QUERY["valid"]
                             ]))
    @allure.title("Тест формы '{form_type.FORM_NAME}': ввод корректных значений")
    def test_fields_passed(self, form_type, link, name, email, query):
        form = form_type(self.browser, link)
        form.open()
        form.enter_fields(
            name,
            email,
            query
        )
        form.tick_checkbox()
        form.push_button()
        form.has_success_message()

    @pytest.mark.parametrize("wrong_name, email, query",
                             Pairwise([
                                 FIO["invalid"],
                                 EMAIL["valid"],
                                 QUERY["valid"]
                             ]))
    @allure.title("Тест формы '{form_type.FORM_NAME}': неккоретный ввод в поле 'ФИО'")
    def test_name_failed(self, form_type, link, wrong_name, email, query):
        form = form_type(self.browser, link)
        form.open()
        form.enter_fields(
            wrong_name,
            email,
            query
        )
        form.tick_checkbox()
        form.approve_error("ФИО")
        form.button_is_desabled()

    @allure.title("Тест формы 'Задай вопрос': неккоретный ввод в поле 'Ваш E-mail'")
    @pytest.mark.parametrize("name, wrong_email, query",
                             Pairwise([
                                 FIO["valid"],
                                 EMAIL["invalid"],
                                 QUERY["valid"]
                             ]))
    @allure.title("Тест формы '{form_type.FORM_NAME}': неккоретный ввод в поле 'Ваш E-mail'")
    def test_email_failed(self, form_type, link, name, wrong_email, query):
        form = form_type(self.browser, link)
        form.open()
        form.enter_fields(
            name,
            wrong_email,
            query
        )
        form.tick_checkbox()
        form.approve_error("Ваш E-mail")
        form.button_is_desabled()

    @pytest.mark.parametrize("name, email, wrong_query",
                             Pairwise([
                                 FIO["valid"],
                                 EMAIL["valid"],
                                 QUERY["invalid"]
                             ]))
    @allure.title("Тест формы '{form_type.FORM_NAME}': неккоретный ввод в поле '{form_type.HELPER_TEXT}'")
    def test_query_failed(self, form_type, link, name, email, wrong_query):
        form = form_type(self.browser, link)
        error_field = form.HELPER_TEXT
        form.open()
        form.enter_fields(
            name,
            email,
            wrong_query
        )
        form.tick_checkbox()
        form.approve_error(error_field)
        form.button_is_desabled()

    @pytest.mark.parametrize("name, email, query",
                             Pairwise([
                                 FIO["valid"],
                                 EMAIL["valid"],
                                 QUERY["valid"]
                             ]))
    @allure.title("Тест формы '{form_type.FORM_NAME}': оставление чекбокса пустым")
    def test_empty_checkbox(self, form_type, link, name, email, query):
        form = form_type(self.browser, link)
        form.open()
        form.enter_fields(
            name,
            email,
            query
        )
        form.button_is_desabled()

    @allure.title("Тест формы '{form_type.FORM_NAME}':оставление всех полей и чекбокса пустыми")
    def test_all_empty(self, form_type, link):
        form = form_type(self.browser, link)
        form.open()
        form.button_is_desabled()
