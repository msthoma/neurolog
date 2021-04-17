from typing import List

from src.add2x2.manager import Add2x2Example


class Evaluator(object):

    def __init__(self):
        pass

    def evaluate(self, facts: List[str], target: Add2x2Example) -> bool:

        row1_sum = target.label[0]
        row2_sum = target.label[1]
        col1_sum = target.label[2]
        col2_sum = target.label[3]

        arguments = [0, 0, 0, 0]
        for fact in facts:
            position = int(fact[5])
            digit = int(fact[3])
            arguments[position - 1] = digit

        if arguments[0] + arguments[1] == row1_sum and arguments[2] + arguments[3] == row2_sum and \
                arguments[0] + arguments[2] == col1_sum and arguments[1] + arguments[3] == col2_sum:
            return True

        return False
