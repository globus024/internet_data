from dotenv import dotenv_values

config = dotenv_values(".env")


EMAIL = config['EMAIL']
PASSWORD = config['PASSWORD']