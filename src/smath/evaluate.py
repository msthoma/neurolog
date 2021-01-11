
from typing import List
from smath.manager import MathExample
from utilities import computeFunction
from smath.local_params import number_of_symbols

class Evaluator(object):

    def __init__(self):
        pass

    def evaluate(self, facts:List[str], target:MathExample)->bool:

        index = 0
        arguments = [None] * number_of_symbols
        for fact in facts:
            position = int(fact[5])
            symbol = int(fact[3])
            arguments[position-1] = symbol
            index += 1
        return computeFunction(arguments) == target.label