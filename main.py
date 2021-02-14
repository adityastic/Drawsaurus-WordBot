from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys


def get_element_by_xpath(driver, element_xpath):
    try:
        return WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, element_xpath)))
    except TimeoutException:
        return None


def login_user(driver, username):
    login_input = get_element_by_xpath(
        driver,
        '/html/body/div[2]/div/div/div[2]/div[1]/form/input[1]'
    )

    if login_input is not None:
        login_input.send_keys(username)
        login_input.send_keys(Keys.ENTER)
        return True
    return False


def fill_password(driver, password):
    password_input = get_element_by_xpath(driver, '/html/body/div[1]/div/div/div[1]/div/form/label/input')

    if password_input is not None:
        password_input.send_keys(password)
        password_input.send_keys(Keys.ENTER)
        return True
    return False


def create_room(driver, room_name, room_password):
    create_room_button = get_element_by_xpath(driver, '/html/body/div[1]/div/div/div/div[1]/div[2]/button[2]')

    if create_room_button is not None:
        create_room_button.click()
        room_name_input = get_element_by_xpath(driver, '/html/body/div[2]/div/div/form/label[1]/input')

        if room_name_input is not None:
            room_name_input.send_keys(room_name)
            driver.find_element_by_xpath('/html/body/div[2]/div/div/form/label[2]/div/select/option[2]').click()
            password_input = get_element_by_xpath(driver, '/html/body/div[2]/div/div/form/label[3]/input')

            if password_input is not None:
                password_input.send_keys(room_password)

                start_playing_button = get_element_by_xpath(driver, '/html/body/div[2]/div/div/form/button[2]')
                start_playing_button.click()

                return driver.current_url


def find_items_by_class(driver, class_to_find):
    items = [item.text for item in driver.find_elements_by_class_name(class_to_find)]
    print(items)


def find_still_playing(driver, class_to_find):
    try:
        still_playing = driver.find_element_by_xpath(class_to_find)
    except NoSuchElementException:
        still_playing = None

    print('SP', still_playing)
    if still_playing is not None:
        still_playing.click()


player1Browser = webdriver.Firefox(
    executable_path='./drivers/geckodriver'
)

player2Browser = webdriver.Firefox(
    executable_path='./drivers/geckodriver'
)

player1Browser.get('https://www.drawasaurus.org')

if login_user(player1Browser, 'Aditya'):
    room_link = create_room(player1Browser, 'ARRoom', 'password')
    print('Room Link:', room_link)

    player2Browser.get(room_link)
    if login_user(player2Browser, 'Rupal'):
        if fill_password(player2Browser, 'password'):
            ready_button_pl1 = get_element_by_xpath(player1Browser,
                                                    '/html/body/div[1]/div/div/div/div[1]/div/div[3]/div[1]/div/div[1]/button[1]')
            ready_button_pl2 = get_element_by_xpath(player2Browser,
                                                    '/html/body/div[1]/div/div/div/div[1]/div/div[3]/div[1]/div/div[1]/button[1]')
            ready_button_pl2.click()
            ready_button_pl1.click()

            for i in range(15):
                print('execution', i)
                find_items_by_class(player1Browser, 'c-word-picker__word')
                find_items_by_class(player2Browser, 'c-word-picker__word')

                find_still_playing(player1Browser, '/html/body/div[1]/div/div/div[1]/div/button')
                find_still_playing(player2Browser, '/html/body/div[1]/div/div/div[1]/div/button')

                find_still_playing(player1Browser,
                                   '/html/body/div[1]/div/div/div/div[1]/div/div[3]/div[1]/div/div[1]/button[1]')
                find_still_playing(player2Browser,
                                   '/html/body/div[1]/div/div/div/div[1]/div/div[3]/div[1]/div/div[1]/button[1]')

            player1Browser.close()
            player2Browser.close()
