from Api import Api
from Welcome import Welcome
from Breakthrough import Breakthrough
from WeeklyPractice import WeeklyPractice
import time

class Fucker:
    def __init__(self):
        self.api = Api()
        self.will_continue = True

    def welcome(self):
        wc = Welcome(self.api)
        return wc.welcome()

    # 闯关答题
    def breakthrough(self):
        bt = Breakthrough(self.api)
        bt.breakthrough()

    # 每周一练
    def weeklypractice(self):
        wp = WeeklyPractice(self.api)
        wp.weeklypractice()

    # 执行任务
    def execute(self):
        func = self.welcome()
        if not func[0] and not func[1]:
            print('所有任务已完成，3秒后退出程序')
            time.sleep(3)
            self.will_continue = False
        else:
            if func[0]:
                print('开始每周一练')
                self.weeklypractice()
            if func[1]:
                print('开始闯关答题')
                self.breakthrough()