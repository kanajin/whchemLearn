import random
import json

class Exam:
    def get_answer_selfadapting(self, subject, answer_list, type):
        def guess_answer(subject):
            def guess_A_or_B():
                return "AB"[random.randint(0,1)]
            def guess_danxuan():
                return chr(random.randint(65,68))
            def guess_duoxuan():
                return "A,B,C,D,E,F,G"[0: random.randrange(2, 13, 2)]
            answer = ''
            if(subject['txstr'] == '判断类'):
                answer = guess_A_or_B()
            elif(subject['txstr'] == '单选类'):
                answer = guess_danxuan()
            else:
                answer = guess_duoxuan()
            return answer
            
        def self_adapting_return(subject, answer_list, type):
            # 通过题面找答案
            if type == 0:
                if(not subject['title'] in answer_list):
                    return guess_answer(subject)
                else:
                    return answer_list[subject['title']]['answers'].replace(';', ',')
            # 通过id找答案
            else:
                if(not str(subject['tmid']) in answer_list):
                    return guess_answer(subject)
                else:
                    return answer_list[str(subject['tmid'])]['answers'].replace(';', ',')

        return self_adapting_return(subject, answer_list, type)

    def get_answer(self, subject_list, answer_list, type):
        return json.dumps([
            {
                'tmid': x['tmid'],
                'answer': self.get_answer_selfadapting(x, answer_list, type)
            } for x in subject_list
        ])