import logging
from Api import Api
import json
from OperateSubject import OperateSubject
import random
import time

class Breakthrough:
    def __init__(self, api: Api):
        self.api = api
        self.subject_list = OperateSubject.load_subject('breakthroughsubject.json')

    # 获取闯关答题未完成的项目，返回一个list
    def get_nopass_id(self):
        breakthroughlist = self.api.get_breakthrough_nopass()
        return [x['PointLevelId'] for x in filter(lambda e: e['IsPassed']==False, breakthroughlist)]

    # 获取题目
    def get_subject(self, id):
        breakthrough_subject_list = self.api.get_breakthrough_subject(id)
        return [(
            {
                "tmid": x.pop("Tm_ID"), 
                "txstr": x.pop("Tm_BaseTx"), 
                "title": x.pop("Title"),
                "options": x.pop("Options"),
            }
        ) for x in breakthrough_subject_list]

    # 查找答案
    def get_subject_answer(self, subject_list):
        def guess_danxuan():
            return chr(random.randint(65,68))
        def guess_duoxuan():
            return "A,B,C,D,E,F,G"[0: random.randrange(2, 13, 2)]

        def get_answer(subject):
            if(not subject['title'] in self.subject_list):
                return guess_answer(subject)
            else:
                return self.subject_list[subject['title']]['answers'].replace(';', ',')
        # 如果题库中不存在该题，瞎猜一个
        def guess_answer(subject):
            answer = ''
            if(subject['txstr'] == '单选类' or subject['txstr'] == '判断类'):
                answer = guess_danxuan()
            else:
                answer = guess_duoxuan()
            subject['answer'] = answer
            self.temp_subject.append(subject)
            return answer

        return json.dumps([
            {
                'tmid': x['tmid'],
                'answer': get_answer(x)
            } for x in subject_list
        ])

    # 提交答案并判断是否通关
    def get_submit(self, id, subject_list):
        submit = {
            'level': id,
            'answer': self.get_subject_answer(subject_list),
            'second': '20'
        }
        resultdata = self.api.breakthrough_submit(submit)
        result = self.api.is_breakthrough_passed(resultdata)
        if result['result']:
            return result['IsPass']
        else:
            return False

    # 答题总接口
    def dealbreakthrough(self, id):
        subject_list = self.get_subject(id)
        time.sleep(15)
        ispassed = self.get_submit(id, subject_list)
        if not ispassed:
            self.dealbreakthrough()
        else:
            print('success')

    # 闯关答题总接口
    def breakthrough(self):
        nopass = self.get_nopass_id()
        for id in nopass:
            self.dealbreakthrough(id)