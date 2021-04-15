import torch

from src.abstract_translator import AbstractTranslator
from src.member.abducibles import abducibles, exclusive
from src.member.evaluate import Evaluator
from src.member.local_params import number_of_arguments
from src.member.manager import MemberManager
from src.networks.mnist_nets import COMP_NET
from src.params import useGPU
from src.run import scenario_test

network = COMP_NET()
if useGPU:
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    network.to(device)

translator = AbstractTranslator(abducibles, exclusive)
dataManager = MemberManager()
outputClasses = [10] * number_of_arguments
evaluator = Evaluator()
scenario = 'member/' + str(number_of_arguments)
# model_name = 'model_samples_3000_iter_400_epoch_1.mdl'
model_name = 'model_samples_3000_iter_9000_epoch_3.mdl'

if __name__ == '__main__':
    scenario_test(network, outputClasses, translator, dataManager, scenario, model_name, evaluator)
