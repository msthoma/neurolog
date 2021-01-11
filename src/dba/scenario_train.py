
import torch
from networks.mnist_nets import COMP_NET
from abstract_translator import AbstractTranslator
from dba.abduction import Abduction
from dba.manager import DBAManager
from dba.local_params import number_of_symbols
from params import useGPU, sicstus_bin
from run import scenario_train
from dba.abducibles import abducibles, exclusive 

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