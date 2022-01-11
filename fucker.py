import requests

s = requests.Session()
s.post

class Fucker:
    def __init__(self):
        self.baseAddress = "https://learning.whchem.com:4443/"
        self.defaultHeader = "User-Agent", "Mozilla /5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"
        self.user = {"username": "00024849", "password": "ytpu2021"}

    async def login(self, session):
        session.post(self.baseAddress + "Api/User/Login", data=self.user)