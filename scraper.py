from typing import Dict
import json
import requests
from const import LOG_IN_URL, HOME_URL
from model.user import User
from bs4 import BeautifulSoup
from selenium import webdriver

class EnelMedSession:
    def __init__(self):
        self.headers = {
            "Authority": "online.enel.pl",
            "cache-control": "max-age=0",
            "sec-ch-ua": 'Google Chrome";v="87", " Not;A Brand";v="99", "Chromium";v="87',
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'",
            "sec-ch-ua-mobile": '?0',
            "Upgrade-Insecure-Requests": "1",
            "sec-fetch-site": "none",
            "sec-fetch-mode": "cors",
            "sec-fetch-user": '?1',
            "sec-fetch-dest": "empty",
            'origin': 'https://online.enel.pl',
            "Accept": 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            "Accept-Language":'en-GB,en;q=0.9,en-US;q=0.8,pl;q=0.7',
            "Accept-Encoding": "gzip, deflate"
                        }
        self.session = requests.Session()


def create_cookies_header(cookies_dict: Dict) -> str:
    result_str = ""
    for cookie_dict in cookies_dict:
        result_str += f"{cookie_dict['name']}={cookie_dict['value']};"
    return result_str


def login(user: User, enel_session: EnelMedSession, driver: webdriver) -> int:
    driver.get(LOG_IN_URL)
    all_cookies = driver.get_cookies()
    driver.close()
    cookies_str = create_cookies_header(all_cookies)
    enel_session.headers['cookie'] = cookies_str
    payload = {"Login": user.username, "Password": user.password, "IsAcceptedRule":"true"}
    response = enel_session.session.post(LOG_IN_URL, headers=enel_session.headers, data=payload)
    print(response.text)


enelmed_sess = EnelMedSession()

with open ('.creds.json', 'r') as cred_file:
    credentials = json.load(cred_file)
    user = User(username=credentials['login'], password=credentials['password'])
    driver = webdriver.Chrome()
    login(user=user, enel_session=enelmed_sess, driver=driver)

