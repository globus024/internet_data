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


# 2) Написать программу, которая собирает «Новинки» с сайта техники mvideo и складывает данные в БД.
# Магазины можно выбрать свои. Главный критерий выбора: динамически загружаемые товары


if __name__ == '__main__':

    chrome_options = Options()
    chrome_options.add_argument('start-maximized')
    chrome_options.headless = True

    driver = webdriver.Chrome(options=chrome_options, executable_path='./chromedriver.exe')

    driver.get('https://www.mvideo.ru/')
    div_novinki = driver.find_element_by_xpath(
        '//div[contains(@data-block-id,"Novinki")]')

    while True:
        li_tags = div_novinki.find_element_by_xpath('//li[contains(@class,"gallery-list-item")]')



    # mail_model = MailModel('less5','mailru')
    # mail_model.run(res)
