import json

class OperateSubject:
    def load_subject(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            subject_list = json.load(f)
        return subject_list

    