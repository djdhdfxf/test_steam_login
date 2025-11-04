import random
import string
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def random_string(length=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))


def test_invalid_login(driver):
    # открываем главную страницу стим
    driver.get("https://store.steampowered.com/?l=russian")

    # найти кнопку войти, благо локатор не понадобился и он так справился
    # но если у нас так же будет проблема с локализацией,то вот пример
    # как можно по xpath находить
    login_button = driver.find_element(By.XPATH, "//a[contains(@class, 'global_action_link')]")
    # login_button = driver.find_element(By.LINK_TEXT, "войти")
    login_button.click()

    # ждём загрузки страницы
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, "//input[contains(@class, '_2GBWeup5cttgbTw8FM3tfx') and @type='text']")))

    input_fields = driver.find_elements(By.TAG_NAME, "input")
    print(f"Найдено {len(input_fields)} полей вода")

    # вводим неверные данные,через генерацию рандомных числе и символов
    username_value = f"user_{random_string(6)}"
    password_value = f"pass{random_string(8)}"
    username = driver.find_element(By.XPATH, "//input[contains(@class, '_2GBWeup5cttgbTw8FM3tfx') and @type='text']")
    password = driver.find_element(By.XPATH,
                                   "//input[contains(@class, '_2GBWeup5cttgbTw8FM3tfx') and @type='password']")
    username.send_keys(username_value)
    password.send_keys(password_value)

    # нажимаем кнопку войти
    sign_in_button = driver.find_element(By.XPATH,
                                         "//button[contains(@class, 'DjSvCZoKKfoNSmarsEcTS') and @type='submit']")
    sign_in_button.click()

    error_mesage = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, "//*[contains(text(), 'Пожалуйста, проверьте свой пароль и имя аккаунта и попробуйте снова.')]"))
    )

    # проверяем текст ошибки будет она или нет
    assert "ошибка" in error_mesage.text.lower() or "пожалуйста, проверьте свой пароль и имя аккаунта и попробуйте снова." in error_mesage.text.lower()
