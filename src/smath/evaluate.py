from typing import List

from src.smath.local_params import number_of_symbols
from src.smath.manager import MathExample
from src.utilities import computeFunction


class Evaluator(object):

    def __init__(self):
        pass

    def evaluate(self, facts: List[str], target: MathExample) -> bool:
        index = 0
        arguments = [None] * number_of_symbols
        for fact in facts:
            position = int(fact[5])
            symbol = int(fact[3])
            arguments[position - 1] = symbol
            index += 1
        return computeFunction(arguments) == target.label
