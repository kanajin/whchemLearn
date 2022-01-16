import requests
import json

class Fucker:
    def __init__(self):
        self.session = requests.Session()
        self.baseAddress = "https://learning.whchem.com:6443/"
        self.defaultHeader = "User-Agent", "Mozilla /5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"
        self.user = {"username": "00024849", "password": "ytpu2021"}
        self.session.headers.update(self.defaultHeader)

    def login(self):
        self.session.headers.update({"authorization":self.session.post(self.baseAddress+"Api/User/Login",data=self.user).json()["data"]['TokenID']})

    