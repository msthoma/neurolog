
from abstract_adbuction import AbstractAbduction
from abstract_translator import AbstractTranslator
from smath.local_params import number_of_symbols

class Abduction(AbstractAbduction):

    def __init__(self, sicstusBin, translator:AbstractTranslator):
        AbstractAbduction.__init__(self, sicstusBin, translator)
        if number_of_symbols == 3:
            self.prepareTheory = 'math3_prepare.pl' 
        elif number_of_symbols == 5:
            self.prepareTheory = 'math5_prepare.pl' 
        
    def prepareInput(self, target):
        with open(self.sicstusBin + 'math_instance.pl', 'w') as f:
            f.write('instance({},[{}],[]).'.format(self.scenario, target.label))