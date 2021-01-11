
from typing import List
from chess.managers.chessISK import ChessExample
from chess.chess_configuration import ChessConfiguration

class ChessISK(object):  

    def __init__(self, configuration:ChessConfiguration):
        self.mate = configuration.getMateProofs()
        self.draw = configuration.getDrawProofs()
        self.safe = configuration.getSafeProofs()
        
    def evaluate(self, facts:List[str], target:ChessExample)->bool:
        W1 = ''
        W2 = ''
        X1 = 0
        Y1 = 0
        X2 = 0
        Y2 = 0
        X3 = 0
        Y3 = 0
        
        invalid = False
        for fact in facts:
            X = int(fact[2])
            Y = int(fact[3])
            P = fact[5:]
            if P != 'bk' and P != 'e':
                if W1 == '':
                    W1 = P
                    (X1,Y1) = (X,Y)
                elif W2 == '':
                    W2 = P
                    (X2,Y2) = (X,Y)
                else:
                    invalid = True
                    break;
            elif P == 'bk':
                if (X3,Y3) == (0,0):
                    (X3,Y3) = (X,Y)
                else:
                    invalid = True
                    break;
                
        if ((X1,Y1) not in target.coordinates) or ((X2,Y2) not in target.coordinates) or ((X3,Y3) not in target.coordinates):
            invalid = True 
            
        if invalid == False:
            if target.label == 'mate':
                return (W1,X1,Y1,W2,X2,Y2,X3,Y3) in self.mate or (W2,X2,Y2,W1,X1,Y1,X3,Y3) in self.mate
        
            if target.label == 'draw':
                return (W1,X1,Y1,W2,X2,Y2,X3,Y3) in self.draw or (W2,X2,Y2,W1,X1,Y1,X3,Y3) in self.draw
    
            if target.label == 'safe':
                return (W1,X1,Y1,W2,X2,Y2,X3,Y3) in self.safe or (W2,X2,Y2,W1,X1,Y1,X3,Y3) in self.safe
        
        return False
