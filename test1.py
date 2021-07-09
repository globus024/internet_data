from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from pprint import pprint
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

chrome_options = Options()
chrome_options.add_argument('start-maximized')
# chrome_options.add_argument('headless')


driver = webdriver.Chrome(executable_path='./chromedriver.exe',options=chrome_options)
driver.get('http://tovar.git/')

# elem = driver.find_element_by_id('user_email')
# elem.send_keys('study.ai_172@mail.ru')
#
# elem = driver.find_element_by_id('user_password')
# elem.send_keys('Password172')
#
# check = driver.find_element_by_id('user_remember_me')
# check.click()

# elem.send_keys(Keys.ENTER)

profile = driver.find_element_by_xpath("//a[contains(@class,'header__top__avatar')]")
driver.get(profile.get_attribute('href'))


elem = driver.find_element_by_id('loginform-email')
elem.send_keys('azamat.khankhodjaev@gmail.com')

elem = driver.find_element_by_id('loginform-password')
elem.send_keys('qazwsx123')
sub = driver.find_element_by_name('save-btn')
sub.click()

# check = driver.find_element_by_id('user_remember_me')
# check.click()
# profile = driver.find_element_by_class_name("text-sm")
# driver.get(profile.get_attribute('href'))
#
# gender = driver.find_element_by_name('user[gender]')
# select = Select(gender)
# select.select_by_value('male')

# gender.submit()

# driver.back()
# driver.forward()
# driver.refresh()

# driver.close()