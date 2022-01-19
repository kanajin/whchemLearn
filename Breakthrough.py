from Api import Api
from OperateSubject import OperateSubject
import time
from Exam import Exam


class Breakthrough:
    def __init__(self, api: Api):
        self.api = api
        self.answer_list = OperateSubject.load_subject(
            'breakthroughsubject.json')

    # 获取闯关答题未完成的项目，返回一个list
    def get_nopass_id(self):
        breakthroughlist = self.api.get_breakthrough_nopass()
        return [x['PointLevelId'] for x in filter(lambda e: e['IsPassed'] == False, breakthroughlist)]

    # 获取题目
    def get_subject(self, id):
        breakthrough_subject_list = self.api.get_breakthrough_subject(id)
        return [(
            {
                "tmid": x["Tm_ID"],
                "txstr": x["Tm_BaseTx"],
                "title": x["Title"],
                "options": x["Options"]
            }
        ) for x in breakthrough_subject_list]

    # 提交答案并判断是否通关
    def get_submit(self, id, subject_list):
        submit = {
            'level': id,
            'answer': Exam.get_answer(subject_list, self.answer_list),
            'second': '20'
        }
        resultdata = self.api.breakthrough_submit(submit)
        result = self.api.is_breakthrough_passed(resultdata)
        if result['Result']:
            return result['Result']['IsPass'] == 1
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
        print('breakthrough success')
