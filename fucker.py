from Api import Api
from Welcome import Welcome
from Breakthrough import Breakthrough
from WeeklyPractice import WeeklyPractice
import sys

class Fucker:
    def __init__(self):
        self.api = Api()

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
        all_func = [0,1,2,3,4]
        if func not in all_func:
            sys.exit(0)

        if func == 1 or func == 2:
            print('功能完善中，请见谅!')

        elif func == 3:
            self.weeklypractice()

        elif func == 4:
            self.breakthrough()

        elif func == 0:
            # 占位
            # 占位
            self.breakthrough()
            self.weeklypractice()