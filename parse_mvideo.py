from selenium.common.exceptions import NoSuchElementException
from string import whitespace
from datetime import datetime, timedelta, date
from selenium.webdriver.remote.webelement import WebElement
import json
CUSTOM_WHITESPACE = (whitespace + "\xa0").replace(" ", "")


class ParseMvideo:


    def __init__(self):
        self.uniq = []

    def parse(self, tags):
        res = []
        for tag in tags:
            try:
                data = json.loads(tag.get_attribute('data-product-info'))
                if data['productId'] in self.uniq:
                    continue
                self.uniq.append(data['productId'])
                res.append(data)
            except Exception:
                continue

        return res




if __name__ == '__main__':
    pass