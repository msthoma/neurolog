
from typing import List
from apply2x2.manager import Apply2x2Example
from utilities import computeFunction

class Evaluator(object):

    def __init__(self):
        pass

    def evaluate(self, facts:List[str], target:Apply2x2Example)->bool:

        digit1 = target.digit1
        digit2 = target.digit2
        digit3 = target.digit3

        operators = [0,0,0,0]
        for fact in facts:
            position = int(fact[5])
            operator = int(fact[3])
            operators[position-1] = operator

        row1_result = computeFunction([digit1, operators[0], digit2, operators[1], digit3])
        row2_result = computeFunction([digit1, operators[2], digit2, operators[3], digit3])
        col1_result = computeFunction([digit1, operators[0], digit2, operators[2], digit3])
        col2_result = computeFunction([digit1, operators[1], digit2, operators[3], digit3])

        if row1_result == target.label[0] and row2_result == target.label[1] and col1_result == target.label[2] and col2_result == target.label[3]:
            return True

        return False