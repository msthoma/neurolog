import torch

from src.abstract_translator import AbstractTranslator
from src.dba.abducibles import abducibles, exclusive
from src.dba.abduction import Abduction
from src.dba.local_params import number_of_symbols
from src.dba.manager import DBAManager
from src.networks.mnist_nets import COMP_NET
from src.params import useGPU, sicstus_bin
from src.run import scenario_train

network = COMP_NET(4)
if useGPU:
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    network.to(device)

translator = AbstractTranslator(abducibles, exclusive)
dataManager = DBAManager()
abduction = Abduction(sicstus_bin, translator)

outputClasses = [4] * number_of_symbols
scenario = 'dba/' + str(number_of_symbols)

scenario_train(network, outputClasses, translator, dataManager, scenario, abduction)
