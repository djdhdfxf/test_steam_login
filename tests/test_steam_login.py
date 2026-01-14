from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from faker import Faker

fake = Faker()

STEAM_URL = "https://store.steampowered.com/"
UNIQUE_ELEMENT = "//form[contains(@action, 'search')]//button[@type='submit']"
# так, выше это ожидание открытия страницы по уникальному элементу
# я решил выбрать лупу в поле поиска.
LOGIN_BUTTON = "//a[contains(@class, 'global_action_link')]"
USERNAME = "//form[.//input[@type='password']]//input[@type='text']"
PASSWORD = "//div[.//input[@type='text'] and .//input[@type='password']]//input[@type='password']"
QUIT_BUTTON = "(//form//button[@type='submit'])[2]"
ERROR_MESAGE = "(//form[.//input[@type='text'] and .//input[@type='password']]//div[normalize-space() and not(.//input) and not(.//button)])[last()]"
#LOAD_PAGE = "//div[contains(@class, '_3BkiHun-mminuTO-Y-zXke')]//input[@type='text']"
WAIT_TIMEOUT = 10


def test_invalid_login(driver):
    # открываем главную страницу стим
    driver.get(STEAM_URL)

    login_button = driver.find_element(By.XPATH, LOGIN_BUTTON)
    login_button.click()

    WebDriverWait(driver, WAIT_TIMEOUT).until(
        EC.presence_of_element_located((By.XPATH, UNIQUE_ELEMENT))
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
        "Пожалуйста, проверьте свой пароль и имя аккаунта и попробуйте снова."
    )
