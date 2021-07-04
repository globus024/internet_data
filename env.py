from dotenv import dotenv_values

config = dotenv_values(".env")


USERNAME = config['USERNAME']
PASSWORD = config['PASSWORD']