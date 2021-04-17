import torch

from src.abstract_translator import AbstractTranslator
from src.apply2x2.abducibles import abducibles, exclusive
from src.apply2x2.abduction import Abduction
from src.apply2x2.manager import Apply2x2Manager
from src.networks.apply2x2_nets import COMP_NET
from src.params import useGPU, sicstus_bin
from src.run import scenario_train

network = COMP_NET()
if useGPU:
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    network.to(device)

translator = AbstractTranslator(abducibles, exclusive)
dataManager = Apply2x2Manager()
abduction = Abduction(sicstus_bin, translator)
outputClasses = [3] * 4
scenario = 'apply2x2'

if __name__ == '__main__':
    scenario_train(network, outputClasses, translator, dataManager, scenario, abduction)
