from local_params import scenario_name
from src.abstract_adbuction import AbstractAbduction
from src.abstract_translator import AbstractTranslator


class Abduction(AbstractAbduction):

    def __init__(self, sicstusBin, translator: AbstractTranslator):
        AbstractAbduction.__init__(self, sicstusBin, translator)
        self.prepareTheory = f"{scenario_name}_prepare.pl"

    def prepareInput(self, target):
        with open(self.sicstusBin + f"{scenario_name}_instance.pl", 'w') as f:
            f.write('instance({},[{}],[]).'.format(self.scenario, target.label))
