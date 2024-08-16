from selenium import webdriver
from selenium.webdriver.chrome.options import Options as OptionsChrome
from selenium.webdriver.firefox.options import Options as OptionsFirefox


class DriverFactory:
    @staticmethod
    def get_driver(config):
        if config["browser"] == "chrome":
            options = OptionsChrome()
            options.add_argument("start-maximized")
            if config["headless_mode"] is True:
                options.add_argument("--headless=new")
            print("\nstart chrome browser for test..")
            driver = webdriver.Chrome(options=options)
            return driver
        elif config["browser"] == "firefox":
            options = OptionsFirefox()
            if config["headless_mode"] is True:
                options.headless = True
            print("\nstart firefox browser for test..")
            driver = webdriver.Firefox(options=options)
            driver.maximize_window()
            return driver
        raise Exception("Provide valid driver name")
