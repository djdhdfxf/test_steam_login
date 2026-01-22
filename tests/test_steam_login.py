from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from faker import Faker

fake = Faker()

STEAM_URL = "https://store.steampowered.com/"
WAIT_TIMEOUT = 10

UNIQUE_ELEMENT = (
    By.XPATH,
    "//form[contains(@action, 'search')]//button[@type='submit']"
)

LOGIN_BUTTON = (
    By.XPATH,
    "//a[contains(@class, 'global_action_link')]"
)

USERNAME = (
    By.XPATH,
    "//form[.//input[@type='password']]//input[@type='text']"
)

PASSWORD = (
    By.XPATH,
    "//div[.//input[@type='text'] and .//input[@type='password']]//input[@type='password']"
)

QUIT_BUTTON = (
    By.XPATH,
    "(//form//button[@type='submit'])[2]"
)

ERROR_MESAGE = (
    By.XPATH,
    "(//form[.//input[@type='text'] and .//input[@type='password']]"
    "//div[normalize-space() and not(.//input) and not(.//button)])[last()]"
)

WAIT_TIMEOUT = 10


def test_invalid_login(driver):
    driver.get(STEAM_URL)

    driver.find_element(*LOGIN_BUTTON).click()

    username_input = WebDriverWait(driver, WAIT_TIMEOUT).until(
        EC.visibility_of_element_located(USERNAME)
    )
    username_input.send_keys(fake.user_name())

    password_input = WebDriverWait(driver, WAIT_TIMEOUT).until(
        EC.visibility_of_element_located(PASSWORD)
    )
    password_input.send_keys(fake.password())

    sign_in_button = WebDriverWait(driver, WAIT_TIMEOUT).until(
        EC.element_to_be_clickable(QUIT_BUTTON)
    )
    sign_in_button.click()

    error_message = WebDriverWait(driver, WAIT_TIMEOUT).until(
        EC.visibility_of_element_located(ERROR_MESAGE)
    )

    WebDriverWait(driver, WAIT_TIMEOUT).until(
        lambda d: error_message.text.strip() != ""
    )

    actual_text = error_message.text.strip()

    EXPECTED_ERROR_TEXT = "Пожалуйста, проверьте свой пароль и имя аккаунта и попробуйте снова."

    assert actual_text == EXPECTED_ERROR_TEXT, (
        f"Текст ошибки не соответствует ожидаемому.\n"
        f"Expected: '{EXPECTED_ERROR_TEXT}'\n"
        f"Actual:   '{actual_text}'"
    )