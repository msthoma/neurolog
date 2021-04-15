from src.abstract_adbuction import AbstractAbduction
from src.abstract_translator import AbstractTranslator
from src.member.local_params import number_of_arguments


class Abduction(AbstractAbduction):

    def __init__(self, sicstusBin, translator: AbstractTranslator):
        AbstractAbduction.__init__(self, sicstusBin, translator)
        if number_of_arguments == 3:
            self.prepareTheory = 'mymember3_prepare.pl'
        elif number_of_arguments == 5:
            self.prepareTheory = 'mymember5_prepare.pl'

    def prepareInput(self, target):
        with open(self.sicstusBin + 'mymember_instance.pl', 'w') as f:
            f.write('instance({},[{},{}],[]).'.format(self.scenario, target.target, target.label))
