import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

CHROME_OPTIONS = ["--window-size=1920,1080"]
IMPLICIT_WAIT = 5

@pytest.fixture
def driver():
    # Настраиваем Chrome через Service
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()

    for opt in CHROME_OPTIONS:
        options.add_argument(opt)

    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(IMPLICIT_WAIT)
    yield driver
    driver.quit()


