import json
from ruts_auto_ui.utils.driver_factory import DriverFactory

CONFIG_PATH = "../config.json"


def link_parser(*classes):
    scope = []
    for cls in classes:
        if "AUTO_LINK" in cls.__dict__:
            for link, args in cls.AUTO_LINK.items():
                config_file = open(CONFIG_PATH)
                browser = DriverFactory.get_driver(json.load(config_file))
                browser.implicitly_wait(3)
                url = cls.BASE_URL + link
                browser.get(url)
                for result in browser.find_elements(*args[1]):
                    scope += [(cls, result.get_attribute(args[0]))]
                browser.quit()
        for link in cls.LINK:
            scope += [(cls, link)]
    return scope
