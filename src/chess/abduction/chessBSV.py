from formula import createDisjunction
from chess.managers.chessBSV_NGA import ChessGoal
from pysdd.sdd import SddNode
from chess.chess_configuration import ChessConfiguration
from chess.abduction.chess_abduction import ChessAbduction
from chess.chess_translator import ChessTranslator

class ChessAbductionBSV(ChessAbduction):

    def __init__(self, sicstusBin, translator:ChessTranslator, configuration:ChessConfiguration):
        ChessAbduction.__init__(self, sicstusBin, translator)
        self.configuration = configuration
        self.prepareTheory = 'chessprepare.pl' 

    def prepareInput(self, target):
        with open(self.sicstusBin + 'input.pl', 'w') as f:
            f.write('input(scenario(1,{},{}),\n'.format(target.label,self.scenario))
            f.write('[\n')
            f.write(']).\n')

    '''
    Runs by reading the cached proofs from the directory "proofs" and without calling SICStus prolog.
    This scenario can be modified to run with SICStus Prolog and without reading the cached proofs by (i) commenting out the method in line 21--42
    and (ii) using the methods in lines 46--73.
    '''
    
    def abduce(self, target:ChessGoal)->SddNode:
        
        if not(target in self.cache):

            if target.label == 'mate':
                proofs = self.configuration.getMateProofs()
            elif target.label == 'draw':
                proofs = self.configuration.getDrawProofs()
            elif target.label == 'safe':
                proofs = self.configuration.getSafeProofs()
            
            index = 0
            disjuncts = list()
            while index < len(proofs):
                proof = proofs[index]
                conjunction = self.convertProofToAbductiveFormula(proof)
                disjuncts.append(conjunction)
                index += 1

            self.cache[target] = createDisjunction(disjuncts)
        
        return self.cache[target]     
    
