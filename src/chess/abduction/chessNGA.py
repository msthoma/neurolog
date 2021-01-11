

from formula import createDisjunction
from chess.managers.chessBSV_NGA import ChessGoal
import subprocess
from pysdd.sdd import SddNode
from chess.abduction.chess_abduction import ChessAbduction
from chess.chess_translator import ChessTranslator
        
class ChessAbductionNGA(ChessAbduction):

    def __init__(self, sicstusBin, translator:ChessTranslator):
        ChessAbduction.__init__(self, sicstusBin, translator)
        self.prepareTheory = 'chessprepare.pl' 
         
    def abduce(self, target:ChessGoal, observations:list)->SddNode:
        key = str(observations) + '_' + target.label
        if not(key in self.cache): 
            self.cache[key] = self.callSicstus(target, observations) 
        return self.cache[key]
    
    def callSicstus(self, target, observations:list)->SddNode:
        self.command = self.sicstusBin + 'sicstus ' + '--noinfo -l ' + self.sicstusBin + 'abduction ' + '-l ' + self.sicstusBin + self.prepareTheory + ' ' + '--goal "go."'
        self.scenario += 1
        self.prepareInput(target,observations)

        process = subprocess.Popen(self.command, stdout=subprocess.PIPE, shell=True)
        process.wait()
        
        proofs = self.translator.importSicstusProofs(self.sicstusBin + 'proofs/{}.txt'.format(self.scenario))
        index = 0
        disjuncts = list()
        while index < len(proofs):
            proof = proofs[index]
            conjunction = self.convertProofToAbductiveFormula(proof)
            disjuncts.append(conjunction)
            index += 1

        return createDisjunction(disjuncts) 
    
    def prepareInput(self, target,observations:list):
        with open(self.sicstusBin + 'input.pl', 'w') as f:
            f.write('input(scenario(3,{},{}),\n'.format(target.label, self.scenario))
            f.write('[\n')
            index = 0
            for observation in observations:
                f.write('\t soft({})'.format(observation))
                if index < len(observations) - 1:
                    f.write(',')
                index += 1
                f.write('\n')
            f.write(']).\n')
