from Api import Api


class Welcome:
    def __init__(self, api: Api):
        self.api = api

    def get_task_list(self):
        def will_show(taskid):
            hit = [2, 7, 11, 14]
            return taskid in hit

        all_tasklist = self.api.get_task_list()
        return filter(lambda x: will_show(x['TaskType']), all_tasklist)

    def print_task_list(self, tasklist):
        def print_task(task):
            print(f"{task['Name']}: 已得 {task['IntegralHave']} 分，共 {task['IntegralMax']} 分")

        count = 1
        for task in tasklist:
            print(count, end='. ')
            print_task(task)
            count += 1

    def welcome(self):
        task_todo = self.get_task_list()
        self.print_task_list(task_todo)
        return int(input('请选择需要完成的项目(输入0表示全做): '))