# Azamat Khankhodjaev
# 25.09.2020

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from parse_mvideo import ParseMvideo
from mvideo_model import MvideoModel
# 2) Написать программу, которая собирает «Новинки» с сайта техники mvideo и складывает данные в БД.
# Магазины можно выбрать свои. Главный критерий выбора: динамически загружаемые товары


if __name__ == '__main__':

    chrome_options = Options()
    chrome_options.add_argument('start-maximized')
    chrome_options.headless = False

    driver = webdriver.Chrome(options=chrome_options, executable_path='./chromedriver.exe')

    driver.get('https://www.mvideo.ru/')

    parse_mvideo = ParseMvideo()
    result_set = []
    next, current = '', ''
    i = 0
    while i < 10:

        div_exist = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (By.XPATH, '//div[contains(@data-block-id,"Novinki")]')))


        actions = ActionChains(driver)
        actions.move_to_element(div_exist)
        actions.perform()
        li_tags = driver.find_elements_by_xpath(
            '//div[contains(@data-block-id,"Novinki")]//li[contains(@class,"gallery-list-item")]//a')

        result_set.extend(parse_mvideo.parse(li_tags))
        next_link = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (By.XPATH, '//div[contains(@data-block-id,"Novinki")]//a[contains(@class,"next-btn")]')))
        if "disabled" in next_link.get_attribute('class'):
            break
        next_link.click()
        i += 1

    mail_model = MvideoModel('less5','mvideo')
    mail_model.run(result_set)
    driver.close()