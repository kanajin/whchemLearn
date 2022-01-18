import logging
import requests
import json

class Api:
    base_url = 'https://learning.whchem.com:6443/'
    url_breakthrough_nopass = base_url+'Api/PointAnswer/GetPointAnswerDetail'
    url_breakthrough_getsubcjet = base_url+'Api/PointAnswer/GetPointAnswerQuestion'
    url_breakthrough_submit = base_url+'Api/PointAnswer/SubmitPointAnswer'
    url_breakthrough_result = base_url+'Api/PointAnswer/GetPointAnswerResult'

    def __init__(self):
        self.session = requests.Session()
        self.header = {'User-Agent': 'Mozilla /5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'}
        
    # 登录，并保存登录信息
    def login(self):
        def get_usr_info():
            with open('usr.json', 'r', encoding='utf-8') as usr_file:
                usr_dict = json.load(usr_file)
            return usr_dict

        def create_usr():
            with open('usr.json', 'w', encoding='utf-8') as f:
                usr_dict = {
                    'username': input('enter username: '),
                    'password': input('enter password: ')
                }
                json.dump(usr_dict, f)
            return usr_dict

        def login_error(login_state):
            print(login_state['msg'])
        
        def dealwith_response(login_state):
            if login_state['state'] != 'success':
                login_error(login_state)
            else:
                tokenid = login_state['data']['TokenID']
                self.session.headers.update({'authorization': tokenid})
                print('success')
        
        login_url = 'https://learning.whchem.com:6443/Api/User/Login'
        usr_dict = {}
        try:
            usr_dict = get_usr_info()
        except FileNotFoundError:
            usr_dict = create_usr()
        login_response = self.Post(login_url, usr_dict).json()
        dealwith_response(login_response)

    # 获取闯关答题未完成项目，返回list
    def get_breakthrough_nopass(self):
        response = self.Post(Api.url_breakthrough_nopass, {"pageSize": "2000", "pageIndex": "0"})
        return response.json()['data']['list']

    # 获取闯关答题题目，返回题目list
    def get_breakthrough_subject(self, id):
        response = self.Post(Api.url_breakthrough_getsubcjet, {"level": id, "isExercise": "false"})
        return response.json()['data']['list']

    # 闯关答题提交
    def breakthrough_submit(self, submit):
        response = self.Post(Api.url_breakthrough_submit, submit)
        return response.json()['data']

    # 判断闯关答题是否通关
    def is_breakthrough_passed(self, result):
        response = self.Post(Api.url_breakthrough_result, result)
        return response.json()['data']

    def Get(self, *args, **kwargs):
        return self.session.get(*args, **kwargs)

    def Post(self, *args, **kwargs):
        return self.session.post(*args, **kwargs)