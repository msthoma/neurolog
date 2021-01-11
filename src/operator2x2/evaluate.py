
from typing import List
from operator2x2.manager import Operator2x2Example
from utilities import computeFunction

class Evaluator(object):

    def __init__(self):
        pass
    
    def evaluate(self, facts:List[str], target:Operator2x2Example)->bool:

        row1_sum = target.label[0]
        row2_sum = target.label[1]
        col1_sum = target.label[2]
        col2_sum = target.label[3]

        arguments = [0,0,0,0,0,0,0,0]
        
        for fact in facts:
            position = int(fact[5])
            digit = int(fact[3])
            arguments[position-1] = digit
                 
        result1 = computeFunction([arguments[0], arguments[4], arguments[1]])
        result2 = computeFunction([arguments[2], arguments[5], arguments[3]])         
        result3 = computeFunction([arguments[0], arguments[6], arguments[2]])
        result4 = computeFunction([arguments[1], arguments[7], arguments[3]])

        if result1 == row1_sum and result2 == row2_sum and result3 == col1_sum and result4 == col2_sum:
            return True

        return False