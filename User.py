from Api import Api

class User:
    def __init__(self, api:Api):
        self.api = api
        self.tasklist = None
        self.weeklyscore = 0.0

    # 获取用户信息
    def get_weekly_score(self):
        weekly_score = self.api.get_user_info()
        self.weeklyscore = weekly_score

    # 获取任务列表
    def get_task_list(self):
        def will_show(taskid):
            hit = [2, 7, 11, 14]
            return taskid in hit

        all_tasklist = self.api.get_task_list()
        self.tasklist = filter(lambda x: will_show(x['TaskType']), all_tasklist)

    # 更新用户信息
    def update_user_info(self):
        self.get_task_list()
        self.get_weekly_score()