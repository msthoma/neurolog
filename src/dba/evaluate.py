
from typing import List
from dba.manager import DBAExample
from dba.utilities import computePositiveAndNegativeCases

class Evaluator(object):

    def __init__(self, number_of_symbols:int):
        (self.positive, self.negative) = computePositiveAndNegativeCases(number_of_symbols)
        self.number_of_symbols = number_of_symbols

    def evaluate(self, facts:List[str], target:DBAExample)->bool:

        arguments = [0] * self.number_of_symbols
        for fact in facts:
            position = int(fact[5])
            digit = int(fact[3])
            arguments[position-1] = digit
            if digit == 0 or digit == 1:
                arguments[position-1] = digit 
            elif digit == 3:
                arguments[position-1] = '=' 
            elif fact == 'plus':
                arguments[position-1] =  '+' 
        
        if target.label == True and arguments in self.positive:
            return True
        
        if target.label == False and arguments not in self.positive:
            return True
                
        return False