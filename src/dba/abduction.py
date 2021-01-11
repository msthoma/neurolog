
from abstract_adbuction import AbstractAbduction
from abstract_translator import AbstractTranslator

class Abduction(AbstractAbduction):

    def __init__(self, sicstusBin, translator:AbstractTranslator):
        AbstractAbduction.__init__(self, sicstusBin, translator)
        self.prepareTheory = 'dba_prepare.pl' 
        
    def prepareInput(self, target):
        with open(self.sicstusBin + 'dba_instance.pl', 'w') as f:
            f.write('instance({},[{}],[]).'.format(self.scenario, target.label))
    