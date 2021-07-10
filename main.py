# Azamat Khankhodjaev
# 25.09.2020

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from collections import OrderedDict
from parse_mail import ParserMail
from mail_model import MailModel
from selenium.common.exceptions import StaleElementReferenceException
import env


# 1) Написать программу, которая собирает входящие письма из своего или тестового почтового ящика и сложить данные о письмах в базу данных
# (от кого, дата отправки, тема письма, текст письма полный)
# Логин тестового ящика: study.ai_172@mail.ru
# Пароль тестового ящика: NextPassword172!


if __name__ == '__main__':

    chrome_options = Options()
    chrome_options.add_argument('start-maximized')
    chrome_options.headless = True

    driver = webdriver.Chrome(options=chrome_options, executable_path='./chromedriver.exe')

    driver.get('https://mail.ru/')

    email_input = driver.find_element_by_name('login')
    email_input.send_keys(env.EMAIL)
    button_email = driver.find_element_by_xpath(
        '//form[contains(@class,"body svelte-1eyrl7y")]/button[contains(@class,"button svelte-1eyrl7y")][contains(@data-testid,"enter-password")]')
    if button_email:
        button_email.click()

    password_input = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, '//form//input[@name="password"]')))

    password_input.send_keys(env.PASSWORD)

    button_enter = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH,
                                                                              '//form[contains(@class,"body svelte-1eyrl7y")]/button[contains(@class,"button svelte-1eyrl7y")][contains(@data-testid,"login-to-mail")]')))
    button_enter.click()
    mail_container = WebDriverWait(driver, 100).until(
        EC.presence_of_element_located((By.CLASS_NAME, "layout__main-frame")))

    i, exit_flag = 1, 0
    links, result_set = [], []
    next, current = '', ''

    parser_mail = ParserMail()
    while True:
        # if i > 6:
        #     break
        try:

            a_tags = driver.find_elements_by_class_name('js-tooltip-direction_letter-bottom')
            div_tag = driver.find_element_by_xpath('//div[contains(@class,"dataset__items")]').find_elements_by_tag_name(
                'a')
            current = a_tags[-1].get_attribute('href')
            if current != next:
                next = current
            else:
                if exit_flag > 3:
                    break
                exit_flag += 1

            result_set.extend(parser_mail.parse(div_tag))

            actions = ActionChains(driver)
            actions.move_to_element(a_tags[-1])
            actions.perform()
        except StaleElementReferenceException:
            exit_flag += 1
            continue
        # i += 1

    res = []
    for item in result_set:
        url = item['link']
        driver.get(url)
        password_input = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'js-readmsg-msg')))

        body_msg = driver.find_element_by_class_name('js-readmsg-msg').text
        item = OrderedDict(item)
        item['body_msg'] = parser_mail.clear_string(body_msg)
        res.append(dict(item))

    mail_model = MailModel('less5','mailru')
    mail_model.run(res)
# for i in range(5):
#
#
