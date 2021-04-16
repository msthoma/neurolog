from src.abstract_adbuction import AbstractAbduction
from src.abstract_translator import AbstractTranslator


class Abduction(AbstractAbduction):

    def __init__(self, sicstusBin, translator: AbstractTranslator):
        AbstractAbduction.__init__(self, sicstusBin, translator)
        self.prepareTheory = 'smaller_than_prepare.pl'

    def prepareInput(self, target):
        with open(self.sicstusBin + 'smaller_than_instance.pl', 'w') as f:
            f.write('instance({},[{},{}],[]).'.format(self.scenario, target.digit2, target.label))
