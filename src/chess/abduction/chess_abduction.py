from abstract_adbuction import AbstractAbduction
from chess.chess_translator import ChessTranslator
from pysdd.sdd import SddNode
from formula import createConjunction

class ChessAbduction(AbstractAbduction):
    
    def __init__(self, sicstusBin, translator:ChessTranslator):
        AbstractAbduction.__init__(self, sicstusBin, translator)
    
    def convertProofToAbductiveFormula(self, partial)->SddNode:
        proof = partial.copy()
        non_empty_coordinates = list()
        for abducible in proof:
            x = int(abducible[len('at') + 7])
            y = int(abducible[len('at') + 9])  
            non_empty_coordinates.append((x,y))

        for i in range(1,4):
            for j in range(1,4):
                    if (i,j) not in non_empty_coordinates:
                        empty = 'at(e,({},{}))'.format(i,j)
                        proof.append(empty)
        
        literals = list()
        for abducible in proof:
            literal = self.translator.getSddLiteral(abducible)
            literals.append(literal)
            for negated in self.translator.getMutuallyExclusiveAbducibles(abducible):
                literals.append(self.translator.getSddLiteral(negated).negate())    
        
        return createConjunction(literals)