from typing import List

from manager import SmallerThanExample


class Evaluator(object):
    def __init__(self):
        pass

    def evaluate(self, facts: List[str], target: SmallerThanExample) -> bool:
        # parse digits
        digit1, digit2 = [int(f[3]) for f in facts]

        if digit1 < digit2 and target.label == True:
            return True

        if digit1 >= digit2 and target.label == False:
            return True

        return False
