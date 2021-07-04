# Azamat Khankhodjaev
# 04.07.2021
from lenta_parser import LentaParse
from mail_parser import MailRuParse
from yandex_parser import YandexParse

if __name__ == "__main__":
    url = "https://lenta.ru/"
    parser = LentaParse(url)
    parser.run()

    url = "https://news.mail.ru/"
    parser = MailRuParse(url)
    parser.run()

    url = "https://yandex.ru/news/"

    parser = YandexParse(url)
    parser.run()
