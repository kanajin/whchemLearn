import random
from re import sub
import requests
import json

class Fucker:
    def __init__(self, usr, pwd):
        self.session = requests.Session()
        self.baseAddress = 'https://learning.whchem.com:6443/'
        self.defaultHeader = {'User-Agent': 'Mozilla /5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'}
        self.user = {'username': usr, 'password': pwd}
        self.session.headers.update(self.defaultHeader)
        self.subject_list = self.get_subject_list()
        self.update_subject_list = False
        self.temp_subject = []

    # 登录并保存登录信息
    def login(self):
        tokenid = self.session.post(self.baseAddress+'Api/User/Login',data=self.user).json()['data']['TokenID']
        self.session.headers.update({'authorization':tokenid})

    # 将题库载入进内存
    def get_subject_list(self):
        with open('subjectlist.json', 'r', encoding='utf-8') as f:
            subject_list = json.load(f)
        return subject_list

    # 获取未完成的任务，返回一个filter对象
    def get_mission_nopass(self):
        mission_list = self.session.get(self.baseAddress+"Api/Common/Task/GetTaskList", data={"taskGroup": "0"}).json()['data']['list']
        return filter(lambda e: e['LimitIntegral'] != e['Integral'] and e["TaskType"] != 12, mission_list)

    # 获取闯关答题未完成的项目，返回一个list
    def get_breakthrough_nopass_id(self):
        breakthroughlist = self.session.post(self.baseAddress+"Api/PointAnswer/GetPointAnswerDetail", data={"pageSize": "2000", "pageIndex": "0"}).json()["data"]["list"]
        return [x['PointLevelId'] for x in filter(lambda e: e['CanJoin']==True, breakthroughlist)]

    # 获取闯关答题题目，接收入参为闯关答题ID，在外部迭代调用，返回一个题目列表
    def get_breakthrough_subject(self, breakthrough_id):
        breakthrough_subject_list = self.session.post(self.baseAddress+'Api/PointAnswer/GetPointAnswerQuestion', data={"level": breakthrough_id, "isExercise": "false"}).json()['data']['list']
        return [(
            {
                "tmid": x.pop("Tm_ID"), 
                "txstr": x.pop("Tm_BaseTx"), 
                "title": x.pop("Title"),
                "options": x.pop("Options"),
            }
        ) for x in breakthrough_subject_list]

    # 通过题目列表查找答案，使用题面匹配，返回一个答案列表字符串
    def get_subject_answer(self, breakthrough_subject_list):
        def get_answer(subject):
            if(not subject['title'] in self.subject_list):
                return guess_answer(subject)
            else:
                return self.subject_list[subject['title']]['answers'].replace(';', ',')
        # 如果题库中不存在该题，瞎猜一个
        def guess_answer(subject):
            self.update_subject_list = True
            answer = ''
            if(subject['txstr'] == '单选类' or subject['txstr'] == '判断类'):
                answer = chr(random.randint(65,68))
            else:
                answer = "A,B,C,D,E,F,G"[0: random.randrange(2, 13, 2)]
            subject['answer'] = answer
            self.temp_subject.append(subject)
            return answer

        return str([
            {
                'tmid': x['tmid'],
                'answer': get_answer(x)
            } for x in breakthrough_subject_list
        ])

    # 修改json题库文件
    def update_subject(self):
        with open('subjectlist.json', 'rb+', encoding='utf-8') as f:
            subject_dict = json.load(f)
            map(lambda x: subject_dict.update(x), self.temp_subject)
            f.truncate()
            f.write(json.dumps(subject_dict, ensure_ascii=False))
        print('subject dict updated')
        self.update_subject_list = False

    # 获取闯关答题提交表单，接收入参为闯关答题ID、题目列表和答案列表
    def get_breakthrough_submitdic(self, breakthrough_id, subject_list):
        return {
            'level': breakthrough_id,
            'answer': self.get_subject_answer(subject_list),
            'second': '20'
        }

    # 闯关答题任务
    def breakthrough(self):
        nopass_list = self.get_breakthrough_nopass_id()
        for breakthrough_id in nopass_list:
            subject_list = self.get_breakthrough_subject(breakthrough_id)
            data = self.get_breakthrough_submitdic(breakthrough_id, subject_list)
            breakthrough_response = self.session.post(self.baseAddress+"Api/PointAnswer/SubmitPointAnswer", data=data).json()
            if(self.update_subject_list and breakthrough_response['state']=='success'):
                self.update_subject()
            elif breakthrough_response['state']!='success':
                self.breakthrough()
            else:
                print('success')
