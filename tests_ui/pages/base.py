from selenium.webdriver.common.by import By

class Base:
    BASE_URL = "https://dev-ruts.lad-academy.ru/"

    def __init__(self, browser, url):
        self.url = url
        self.browser = browser

    @classmethod
    def group_elements(cls, keyword: str) -> dict:
        group = {}
        for key, value in cls.__dict__.items():
            if keyword in key:
                group.update({key: value})
        return group

    def enter_data(self, locator: tuple, data: str) -> None:
        self.browser.find_element(*locator).send_keys(data)

    def group_checker(self, text: str, keyword: str):
        if text not in self.group_elements(keyword).values():
            raise ValueError(f'Allowable arguments: {self.group_elements(keyword).values()}')

    def has_text(self, locator: tuple, txt: str) -> None:

        ourtext = self.browser.find_element(*locator).text
        assert ourtext == txt, \
            f"Wrong text: '{ourtext}', must be: '{txt}'"

    def must_be_active(self, locator: tuple, choose: bool = True) -> None:
        item = self.browser.find_element(*locator)
        if choose:
            assert item.is_enabled(), \
                f'Element is not enabled'
        else:
            assert item.is_enabled() is False or "pointer-events-none" in item.get_attribute('class'), \
                f'Element must be disabled'

    def open(self) -> None:
        self.browser.get(self.url)

    def refresh(self) -> None:
        self.browser.refresh()
