from typing import List


def computeFunction(arguments: List) -> int:
    index = 0
    op = -1
    while index < len(arguments):
        if index % 2 == 0:
            if op == -1:
                result = arguments[index]
            else:
                if op == 1:
                    result = result + arguments[index]
                elif op == 2:
                    result = result - arguments[index]
                elif op == 3:
                    result = result * arguments[index]
        else:
            op = arguments[index]
        index += 1
    return result
