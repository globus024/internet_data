# Azamat Khankhodjaev
# 25.09.2020
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import time

chrome_options = Options()
chrome_options.add_argument('start-maximized')
# chrome_options.add_argument('headless')

driver = webdriver.Chrome(options=chrome_options, executable_path='./chromedriver.exe')
driver.get('https://mail.ru/')
email_input = driver.find_element_by_name('login')
email_input.send_keys('study.ai_172@mail.ru')
button_email = driver.find_element_by_xpath('//form[contains(@class,"body svelte-1eyrl7y")]/button[contains(@class,"button svelte-1eyrl7y")][contains(@data-testid,"enter-password")]')
if button_email:
    button_email.click()


password_input =  WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//form//input[@name="password"]')))
password_input.send_keys('NextPassword172!')

button_enter = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//form[contains(@class,"body svelte-1eyrl7y")]/button[contains(@class,"button svelte-1eyrl7y")][contains(@data-testid,"login-to-mail")]')))
button_enter.click()

mail_container = WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CLASS_NAME, "layout__main-frame")))
# a ='''
# document.getElementsByClassName('dataset__items')[0].style.height ='10000px';
# document.getElementsByClassName('dataset__items')[0].style.paddingTop ='5000px';
# window.scrollTo(0, document.body.scrollHeight);
# '''
#
# driver.execute_script(a)
while True:
    a_tags = driver.find_elements_by_class_name('js-tooltip-direction_letter-bottom')
    actions = ActionChains(driver)
    actions.move_to_element(a_tags[-1])
    actions.perform()
    time.sleep(1)

# for i in range(5):
#
#




