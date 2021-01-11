
from typing import List
from chess.utilities import importSicstusProofs

class ChessConfiguration(object):
    
    def __init__(self, dimensionx:int, dimensiony:int, proof:str, piecesToPosition:dict):
        self.proof = proof
        self.piecesToPosition = piecesToPosition
        self.dimensionx = dimensionx
        self.dimensiony = dimensiony
        
    def numberOfPieces(self)->int:
        return len(self.piecesToPosition)
        
    def getPosition(self, piece:str)->int:
        return self.piecesToPosition[piece]
    
    def getBlackKingPosition(self)->int:
        return self.piecesToPosition['bk']
    
    def getEmptyPosition(self)->int:
        return self.piecesToPosition['e']
    
    def getMateProofs(self)->List:
        return importSicstusProofs(self.proof + 'mate.txt')
    
    def getDrawProofs(self)->List:
        return importSicstusProofs(self.proof + 'draw.txt')
    
    def getSafeProofs(self)->List:
        return importSicstusProofs(self.proof + 'safe.txt')
        
    def getOutputClasses(self)->list:
        return [self.numberOfPieces()] * self.dimensionx * self.dimensiony
