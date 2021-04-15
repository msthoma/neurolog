import subprocess

from pysdd.sdd import SddNode

from src.abstract_translator import AbstractTranslator
from src.benchmark_manager import Goal
from src.formula import createConjunction, createDisjunction


class AbstractAbduction(object):
    def __init__(self, sicstusBin, translator: AbstractTranslator):
        self.sicstusBin = sicstusBin
        self.translator = translator
        self.prepareTheory = None
        self.cache = dict()
        self.scenario = 0

    def abduce(self, target: Goal) -> SddNode:
        if not (target in self.cache):
            self.cache[target] = self.callSicstus(target)
        return self.cache[target]

    def callSicstus(self, target: Goal) -> SddNode:
        # self.command = self.sicstusBin + 'sicstus ' + '--noinfo -l ' + self.sicstusBin + 'abduction ' + '-l ' + self.sicstusBin + self.prepareTheory + ' ' + '--goal "go."'
        self.command = '/usr/local/sicstus4.6.0/bin/sicstus ' + '-l ' + self.sicstusBin + 'abduction ' + '-l ' + self.sicstusBin + self.prepareTheory + ' ' + '--goal "go."'

        self.scenario += 1
        self.prepareInput(target)

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

    def convertProofToAbductiveFormula(self, proof) -> SddNode:
        literals = list()
        for abducible in proof:
            literal = self.translator.getSddLiteral(abducible)
            literals.append(literal)
            for negated in self.translator.getMutuallyExclusiveAbducibles(abducible):
                literals.append(self.translator.getSddLiteral(negated).negate())
        return createConjunction(literals)

    def prepareInput(self, target: Goal):
        pass
