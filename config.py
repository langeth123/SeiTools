from loguru import logger
from threading import Thread
import requests
from time import sleep
import random
import string
import inquirer
from termcolor import colored
from inquirer.themes import load_theme_from_dict as loadth

THREAD_RUNNER_SLEEP = 1

class BadDiscordToken(Exception):
    def __init__(self, token, message="Session is dead, try to change token and try again"):
        self.token = token
        self.message = message
        super().__init__(f'[{self.token}] {self.message}')

class MaxTryingsExceed(Exception):
    def __init__(self, message="Max tryings Exceeded"):
        self.message = message
        super().__init__(self.message)


with open(f"data/data.txt", "r", encoding='utf-8') as file:
    DATA = [row.strip() for row in file]
    logger.success(f"Found: {len(DATA)} lines of data for work")

ACCOUNTS = []

for i in DATA:
    try:
        temp_data = i.replace(" ", "").split(":", maxsplit=2)
        if len(temp_data) == 2:
            logger.info(f'[{temp_data[0]}] Runnig thread without proxies')
            ACCOUNTS.append(
                {
                    "address": temp_data[0],
                    "token": temp_data[1]
                }
            )
        elif len(temp_data) == 3:
            logger.info(f'[{temp_data[0]}] Proxy is: {temp_data[2]}')
            ACCOUNTS.append(
                {
                    "address": temp_data[0],
                    "token": temp_data[1],
                    "proxies": {
                        "http"  : f"http://{temp_data[2]}",
                        "https" : f"http://{temp_data[2]}"
                    }
                }
            )
    
    except:
        pass
