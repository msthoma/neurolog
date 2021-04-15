from src.abstract_adbuction import AbstractAbduction
from src.abstract_translator import AbstractTranslator


class Abduction(AbstractAbduction):

    def __init__(self, sicstusBin, translator: AbstractTranslator):
        AbstractAbduction.__init__(self, sicstusBin, translator)
        self.prepareTheory = 'add2x2_prepare.pl'

    def prepareInput(self, target):
        with open(self.sicstusBin + 'add2x2_instance.pl', 'w') as f:
            f.write('instance({},[{},{},{},{}],[]).'.format(self.scenario, target.label[0], target.label[1],
                                                            target.label[2], target.label[3]))
