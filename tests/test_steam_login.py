import random
import string
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from faker import Faker

fake = Faker()

STEAM_URL = "https://store.steampowered.com/"
SEARCH_BUTTON = "//form[contains(@action, 'search')]//button[@type='submit']"
# так, выше это ожидание открытия страницы по уникальному элементу
# я решил выбрать лупу в поле поиска.
LOGIN_BUTTON = "//a[contains(@class, 'global_action_link')]"
USERNAME = "//div[contains(@class,'_3BkiHun-mminuTO-Y-zXke')]//input[@type='text']"
PASSWORD = "//div[contains(@class, '_3BkiHun-mminuTO-Y-zXke')]//input[@type='password']"
QUIT_BUTTON = "//button[contains(@class, 'DjSvCZoKKfoNSmarsEcTS') and @type='submit']"
ERROR_MESAGE = "//div[contains(@class, '_1W_6HXiG4JJ0By1qN_0fGZ')]"
LOAD_PAGE = "//div[contains(@class, '_3BkiHun-mminuTO-Y-zXke')]//input[@type='text']"
WAIT_TIMEOUT = 10


def generate_random_string(length=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))


def test_invalid_login(driver):
    # открываем главную страницу стим
    driver.get(STEAM_URL)

    login_button = driver.find_element(By.XPATH, LOGIN_BUTTON)
    login_button.click()

    WebDriverWait(driver, WAIT_TIMEOUT).until(
        EC.presence_of_element_located(
            (By.XPATH, SEARCH_BUTTON)
        )
    )

    username_value = fake.user_name()
    password_value = fake.password()

    driver.find_element(By.XPATH, USERNAME).send_keys(username_value)
    driver.find_element(By.XPATH, PASSWORD).send_keys(password_value)

    # нажимаем кнопку войти
    sign_in_button = driver.find_element(By.XPATH, QUIT_BUTTON)
    sign_in_button.click()

    error_mesage = WebDriverWait(driver, WAIT_TIMEOUT).until(
        EC.visibility_of_element_located((By.XPATH, ERROR_MESAGE))
    )

    WebDriverWait(driver, WAIT_TIMEOUT).until(
        lambda d: error_mesage.text.strip() != ""
    )

    actual_text = error_mesage.text.strip()

    assert actual_text != "", (
        "Ошибка отображается, но текст ошибки пустой"
    )
