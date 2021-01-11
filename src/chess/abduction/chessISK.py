
from chess.chess_translator import ChessTranslator
from chess.abduction.chess_abduction import ChessAbduction
        
class ChessAbductionISK(ChessAbduction):

    def __init__(self, sicstusBin, translator:ChessTranslator):
        ChessAbduction.__init__(self, sicstusBin, translator)
        self.prepareTheory = 'chessprepare.pl' 
    
    def prepareInput(self, target):
        with open(self.sicstusBin + 'input.pl', 'w') as f:
            f.write('input(scenario(2,{},{}),\n'.format(target.label,self.scenario))
            f.write('[\n')
            index = 0
            for (x,y) in target.coordinates:
                f.write('\t hard(at(_,({},{})))'.format(x,y))
                if index < len(target.coordinates) - 1:
                    f.write(',')
                index += 1
                f.write('\n')
            f.write(']).\n')
