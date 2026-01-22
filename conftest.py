import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

CHROME_ARGUMENTS = [
    "--incognito",
    "--window-size=1920,1080",
    "--lang=ru-RU",
]

CHROME_PREFS = {
    "intl.accept_languages": "ru,ru_RU"
}

IMPLICIT_WAIT = 5


@pytest.fixture
def driver():
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()

    for arg in CHROME_ARGUMENTS:
        options.add_argument(arg)

    options.add_experimental_option("prefs", CHROME_PREFS)

    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(IMPLICIT_WAIT)

    yield driver
    driver.quit()


