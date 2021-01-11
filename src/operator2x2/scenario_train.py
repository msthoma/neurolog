import torch
from networks.operator2x2_nets import COMP_NET
from operator2x2.abduction import Abduction
from operator2x2.manager import Operator2x2Manager
from abstract_translator import AbstractTranslator
from params import useGPU, sicstus_bin
from run import scenario_train
from operator2x2.abducibles import abducibles, exclusive    
    
network = COMP_NET()
if useGPU:
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    network.to(device)
    
translator = AbstractTranslator(abducibles, exclusive)
dataManager = Operator2x2Manager()
abduction = Abduction(sicstus_bin, translator)
outputClasses = [10] * 4
outputClasses.extend([3] * 4)
scenario = 'operator2x2'

scenario_train(network, outputClasses, translator, dataManager, scenario, abduction)
