import random
import string
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#pytest -v
#pytest -v tests/

STEAM_URL = "https://store.steampowered.com/?l=russian"
LOGIN_BUTTON = "//a[contains(@class, 'global_action_link')]"
USERNAME = "//input[contains(@class, '_2GBWeup5cttgbTw8FM3tfx') and @type='text']"
PASSWORD = "//input[contains(@class, '_2GBWeup5cttgbTw8FM3tfx') and @type='password']"
QUIT_BUTTON = "//button[contains(@class, 'DjSvCZoKKfoNSmarsEcTS') and @type='submit']"
ERROR_MESAGE = "//*[contains(text(), 'Пожалуйста, проверьте свой пароль и имя аккаунта и попробуйте снова.')]"
LOAD_PAGE = "//div[@class='_3BkiHun-mminuTO-Y-zXke']/input[@type='text']"
WAIT_TIMEOUT = 10

def generate_random_string(length=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))


def test_invalid_login(driver):
    # открываем главную страницу стим
    driver.get(STEAM_URL)

    login_button = driver.find_element(By.XPATH, LOGIN_BUTTON)
    # login_button = driver.find_element(By.LINK_TEXT, "войти")
    login_button.click()

    # ждём загрузки страницы
    WebDriverWait(driver, WAIT_TIMEOUT).until(
        EC.presence_of_element_located(
            (By.XPATH, LOAD_PAGE)))

    #input_fields = driver.find_elements(By.TAG_NAME, "input")
    #print(f"Найдено {len(input_fields)} полей вода")

    # вводим неверные данные,через генерацию рандомных числе и символов
    username_value = f"user_{generate_random_string(6)}"
    password_value = f"pass{generate_random_string(8)}"

    driver.find_element(By.XPATH, USERNAME).send_keys(username_value)
    driver.find_element(By.XPATH, PASSWORD).send_keys(password_value)


    # нажимаем кнопку войти
    sign_in_button = driver.find_element(By.XPATH, QUIT_BUTTON)
    sign_in_button.click()

    error_mesage = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, ERROR_MESAGE))
    )

    # проверяем текст ошибки будет она или нет
    EXPECTED_ERROR_TEXT = "пожалуйста, проверьте свой пароль и имя аккаунта и попробуйте снова."

    actual_text = error_mesage.text.lower()

    assert actual_text == EXPECTED_ERROR_TEXT, (
        f" Ошибка текста.\n"
        f"Ожидание: {EXPECTED_ERROR_TEXT}\n"
        f"Получили: {actual_text}")
