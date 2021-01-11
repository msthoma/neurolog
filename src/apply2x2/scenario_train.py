
import torch
from networks.apply2x2_nets import COMP_NET
from abstract_translator import AbstractTranslator
from apply2x2.abduction import Abduction
from apply2x2.manager import Apply2x2Manager
from params import useGPU, sicstus_bin
from run import scenario_train
from apply2x2.abducibles import abducibles, exclusive 

network = COMP_NET()
if useGPU:
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    network.to(device)

translator = AbstractTranslator(abducibles, exclusive)
dataManager = Apply2x2Manager()
abduction = Abduction(sicstus_bin, translator)
outputClasses = [3] * 4
scenario = 'apply2x2'

scenario_train(network, outputClasses, translator, dataManager, scenario, abduction)
