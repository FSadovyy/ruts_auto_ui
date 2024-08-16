# pip install selenium-wire
import json
import allure
import pytest
from ruts_auto_ui.utils.driver_factory import DriverFactory
from allure_commons.types import AttachmentType

CONFIG_PATH = "ruts_auto_ui/config.json"
DEFAULT_TIMEOUT = 10

@pytest.fixture(scope='session')
def config():
    config_file = open(CONFIG_PATH)
    return json.load(config_file)

@pytest.fixture(scope='session')
def timeout(config):
    return config["timeout"] if "timeout" in config else DEFAULT_TIMEOUT

@pytest.fixture()
def setup(request, config, timeout):
    if config["browser"] not in ("chrome", "firefox"):
        raise pytest.UsageError("--browser_name should be chrome or firefox")
    browser = DriverFactory.get_driver(config)
    browser.implicitly_wait(timeout)
    request.cls.browser = browser
    before_failed = request.session.testsfailed
    yield
    if request.session.testsfailed != before_failed:
        allure.attach(browser.get_screenshot_as_png(),
                      name="Test failed", attachment_type=AttachmentType.PNG)
    print("\nquit browser..")
    browser.quit()


