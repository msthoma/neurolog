import torch

from src.abstract_translator import AbstractTranslator
from src.networks.operator2x2_nets import COMP_NET
from src.operator2x2.abducibles import abducibles, exclusive
from src.operator2x2.abduction import Abduction
from src.operator2x2.manager import Operator2x2Manager
from src.params import useGPU, sicstus_bin
from src.run import scenario_train

network = COMP_NET()
if useGPU:
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    network.to(device)

translator = AbstractTranslator(abducibles, exclusive)
dataManager = Operator2x2Manager()
abduction = Abduction(sicstus_bin, translator)
outputClasses = [10] * 4  # 10 digits x 4 results
outputClasses.extend([3] * 4)
scenario = 'operator2x2'

if __name__ == '__main__':
    scenario_train(network, outputClasses, translator, dataManager, scenario, abduction)
