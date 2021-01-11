from typing import List
from abstract_translator import AbstractTranslator
from chess.utilities import parseSicstusProof

class ChessTranslator(AbstractTranslator):

    def __init__(self, abducibles:List, mutuallyExclusive):
        AbstractTranslator.__init__(self, abducibles, mutuallyExclusive)
   
    def parseSicstusProof(self, line:str):
        return parseSicstusProof(line)