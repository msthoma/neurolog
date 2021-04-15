import torch

from abducibles import abducibles, exclusive
from abduction import Abduction
from local_params import number_of_arguments
from manager import MemberManager
from src.abstract_translator import AbstractTranslator
from src.networks.mnist_nets import COMP_NET
from src.params import useGPU, sicstus_bin
from src.run import scenario_train

network = COMP_NET()
if useGPU:
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    network.to(device)

translator = AbstractTranslator(abducibles, exclusive)
dataManager = MemberManager()
abduction = Abduction(sicstus_bin, translator)
outputClasses = [10] * number_of_arguments
scenario = 'member/' + str(number_of_arguments)

if __name__ == '__main__':
    scenario_train(network, outputClasses, translator, dataManager, scenario, abduction)
