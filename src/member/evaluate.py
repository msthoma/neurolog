
from typing import List
from member.manager import MemberExample


class Evaluator(object):  

    def __init__(self):
        pass

    def evaluate(self, facts:List[str], target:MemberExample)->bool:        
        
        arguments = list()
        for fact in facts:
            digit = int(fact[3])
            arguments.append(digit)

        if target.target in arguments and target.label == True:
            return True
        
        if not (target.target in arguments) and target.label == False:
            return True
        
        return False