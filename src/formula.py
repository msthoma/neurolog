
from pysdd.sdd import SddNode
from enum import Enum
from builtins import list
from typing import List

class LogicalOperator(Enum):
    Empty = 0
    Conjunction = 1
    Disjunction = 2
    Negation = 3
    
class LogicalType(Enum):
    Variable = 0
    Conjunction = 1
    Disjunction = 2
    Negation = 3

class Formula:
    def __init__(self, ftype:LogicalType, operator:LogicalOperator, variables:list, string:str):
        self.type = ftype
        self.operator = operator
        self.variables = variables
        self.string = string
    def getType(self):
        return self.type
    def getVariables(self) -> list:
        return self.variables
    def getNumberOfVariable(self) -> int:
        return len(self.variables)
    def __str__(self):
        return self.string

class Variable(Formula):
    def __init__(self, value:str):
        Formula.__init__(self, ftype = LogicalType.Variable, operator= LogicalOperator.Empty, variables = [value], string = value)
        self.name = value
    def getName(self)->str:
        return self.name   

def createDisjunction(arguments:List[SddNode]):  
    index = 1
    formula = arguments[0]   
    while index < len(arguments):
        formula = formula.disjoin(arguments[index])
        index +=1 
    return formula
    
def createConjunction(arguments:List[SddNode]):  
    index = 1
    formula = arguments[0]
    while index < len(arguments):
        formula = formula.conjoin(arguments[index])
        index +=1 
    return formula
