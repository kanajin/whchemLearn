from Api import Api
from User import User

class Welcome:
    def __init__(self, api: Api):
        self.api = api
        self.user = User(api)

    # 打印任务列表
    def create_task_list(self, tasklist, weeklyscore):
        def print_task(task):
            print(f"{task['Name']}: 已得 {task['IntegralHave']} 分，共 {task['IntegralMax']} 分")

        count = 1
        todolist = []
        print(f'本周已得{weeklyscore}分')
        for task in tasklist:
            print(count, end='. ')
            print_task(task)
            todolist.append(task['IntegralHave']!=task['IntegralMax'])
            count += 1
        return todolist

    def welcome(self):
        self.user.update_user_info()
        return self.create_task_list(self.user.tasklist, self.user.weeklyscore)