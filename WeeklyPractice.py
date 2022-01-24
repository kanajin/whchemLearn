from Api import Api
from OperateSubject import OperateSubject
import time
from Exam import Exam


class WeeklyPractice:
    def __init__(self, api: Api):
        self.api = api
        self.answer_list = OperateSubject.load_subject('normalsubject.json')

    # 获取每周一练的信息，返回获取题目需要用到的表单
    def get_info(self):
        info = self.api.get_weeklypractice_info()
        weeklist = info['list'][int(time.strftime('%m'))-1]['WeekList']
        all_task = list(filter(lambda x: x['State'] == 'Doing', weeklist))
        if len(all_task) == 0:
            return {}
        else:
            thisweek = list(filter(lambda x: x['State'] == 'Doing', weeklist))[0]
            return {
                'year': str(thisweek['Year']),
                'month': str(thisweek['Month']),
                'week': str(thisweek['Week'])
            }

    # 获取每周一练题目
    def get_subject(self, thisweek):
        subject_list = self.api.get_weeklypractice_subject(thisweek)
        return [
            (
                {
                    "tmid": x["Tm_ID"],
                    "txstr": x["Tm_BaseTx"],
                    "title": x["Title"],
                    "options": x["Options"]
                }
            ) for x in subject_list
        ]

    # 提交答案并判断是否通关
    def get_submit(self, thisweek, subject_list):
        submit = {
            'year': str(thisweek['year']),
            'month': str(thisweek['month']),
            'week': str(thisweek['week']),
            'second': '20',
            'answerstring': Exam().get_answer(subject_list, self.answer_list, 1)
        }
        result_data = self.api.weeklypractice_submit(submit)
        result = self.api.is_weeklypractice_passed(result_data)
        if result['result']:
            return result['result']['Result']['IsAllRight'] == 1
        else:
            return False

    # 答题总接口
    def dealweeklypractice(self, thisweek):
        subject_list = self.get_subject(thisweek)
        time.sleep(15)
        ispassed = self.get_submit(thisweek, subject_list)
        if not ispassed:
            self.dealweeklypractice(thisweek)

    # 每周一练总接口
    def weeklypractice(self):
        thisweek = self.get_info()
        if thisweek:
            self.dealweeklypractice(thisweek)
        print('每周一练已完成')
