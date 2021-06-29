import os
from dotenv import dotenv_values
# pip install python-dotenv

config = dotenv_values(".env")


USERNAME = config['USERNAME']
TOKKEN = config['TOKKEN']

