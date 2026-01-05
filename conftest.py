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

'''import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

IMPLICIT_WAIT = 5
WINDOW_SIZE = "1920,1080"

SAFARI_USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/605.1.15 (KHTML, like Gecko) "
    "Version/18.6 Safari/605.1.15"
)


@pytest.fixture
def driver():
    service = Service(ChromeDriverManager().install())

    options = webdriver.ChromeOptions()
    options.add_argument(f"--window-size={WINDOW_SIZE}")
    options.add_argument(f"user-agent={SAFARI_USER_AGENT}")

    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(IMPLICIT_WAIT)

    yield driver
    driver.quit()'''
