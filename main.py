# Azamat Khankhodjaev
# 25.09.2020
from selenium import webdriver
from lxml.html import fromstring, HtmlElement

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import time

chrome_options = Options()
chrome_options.add_argument('start-maximized')
# chrome_options.add_argument('headless')

driver = webdriver.Chrome(options=chrome_options, executable_path='./chromedriver.exe')
driver.get('https://mail.ru/')
email_input = driver.find_element_by_name('login')
email_input.send_keys('study.ai_172@mail.ru')
button_email = driver.find_element_by_xpath(
    '//form[contains(@class,"body svelte-1eyrl7y")]/button[contains(@class,"button svelte-1eyrl7y")][contains(@data-testid,"enter-password")]')
if button_email:
    button_email.click()

password_input = WebDriverWait(driver, 5).until(
    EC.element_to_be_clickable((By.XPATH, '//form//input[@name="password"]')))
password_input.send_keys('NextPassword172!')

button_enter = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH,
                                                                          '//form[contains(@class,"body svelte-1eyrl7y")]/button[contains(@class,"button svelte-1eyrl7y")][contains(@data-testid,"login-to-mail")]')))
button_enter.click()

mail_container = WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CLASS_NAME, "layout__main-frame")))


class ParserMail:
    def __init__(self):
        self.uniq =[]
    @property
    def template(self):
        data_template = {
            "link": lambda a: a.get_attribute('href'),
            "from": lambda a: a.find_element_by_class_name('ll-crpt').get_attribute('title'),
            "title": lambda a: a.find_element_by_class_name('ll-sj__normal').text,
            'send_date': lambda a: a.find_element_by_class_name('llc__item_date').get_attribute('title'),
        }
        return data_template

    def parse(self, tags):
        res = []
        for tag in tags:
            data ={}
            for key, func in self.template.items():
                try:
                    data[key] = func(tag)
                except NoSuchElementException:
                    continue
            if data['link'] in self.uniq:
                continue
            self.uniq.append(data['link'])
            res.append(data)
        return res


parser_mail = ParserMail()
i = 1
a = 0
links = []
rr = []
next, current = '', ''
while True:
    if i > 10:
        break

    a_tags = driver.find_elements_by_class_name('js-tooltip-direction_letter-bottom')
    div_tag = driver.find_element_by_xpath('//div[contains(@class,"dataset__items")]').find_elements_by_tag_name('a')
    current = a_tags[-1].get_attribute('href')
    if current != next:
        next = current
    else:
        if a > 3:
            break
        a += 1
    rr.extend(parser_mail.parse(div_tag))


    actions = ActionChains(driver)
    actions.move_to_element(a_tags[-1])
    actions.perform()

    # time.sleep(0.5)

for ff in rr:
    print(ff)
    i += 1
# for i in range(5):
#
#
