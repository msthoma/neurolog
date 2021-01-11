from typing import List
from pysdd.sdd import SddManager, Vtree

class AbstractTranslator(object):

    def __init__(self, abducibles:List, mutuallyExclusive):
        self.abduciblesToSddLiterals = dict()
        self.SddLiteralsToOutputNeurons = dict()
        self.outputneuronsToAbducibles = dict()
        self.mutuallyExclusiveDict = dict()
        
        vtree = Vtree(var_count = len(abducibles), var_order = list(range(1, len(abducibles) + 1)), vtree_type="balanced")
        self.sddmanager = SddManager.from_vtree(vtree)
            
        index = 0
        for abducible in abducibles:
            literal = self.sddmanager.literal(index + 1)
            self.abduciblesToSddLiterals[abducible] = literal
            self.SddLiteralsToOutputNeurons[literal] = index
            self.outputneuronsToAbducibles[index] = abducible
            index += 1
            
        for i in range(len(mutuallyExclusive)):
            me = mutuallyExclusive[i]    
            for abducible in me:
                fresh = me.copy()
                fresh.remove(abducible)
                self.mutuallyExclusiveDict[abducible] = fresh
                
    def getSddLiteral(self, abducible:str):
        return self.abduciblesToSddLiterals[abducible] 
            
    def getAbduciblesToSddLiterals(self): 
        return self.abduciblesToSddLiterals 
    
    def getSddLiteralsToOutputNeurons(self): 
        return self.SddLiteralsToOutputNeurons 
    
    def getSddmanager(self):
        return self.sddmanager
    
    def getMutuallyExclusiveAbducibles(self, abducible):
        return self.mutuallyExclusiveDict[abducible]
            
    def parseSicstusProof(self, line:str):
        abducibles = list()
        cont = True
        while cont == True:
            start = line.find('at', 0)
            if start == -1: 
                cont = False
            else: 
                end = line.find(')', 0)
                abducible = line[start:end+1]
                abducibles.append(abducible)
                line = line[end+1:]
        return abducibles

    def importSicstusProofs(self, fileName:str)->List:
        proofs = list()
        fp = open(fileName, 'r')
        for line in fp:
            line = line.rstrip("\n")
            if line.startswith(' <= '):
                proofs.append(self.parseSicstusProof(line))
        return proofs    
            
    def toFact(self, index:int)->str:
        return self.outputneuronsToAbducibles[index]
    
   
