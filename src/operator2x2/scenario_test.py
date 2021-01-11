import torch
from networks.operator2x2_nets import COMP_NET
from abstract_translator import AbstractTranslator
from operator2x2.manager import Operator2x2Manager
from operator2x2.evaluate import Evaluator
from params import useGPU
from run import scenario_test
from operator2x2.abducibles import abducibles, exclusive    

network = COMP_NET()
if useGPU:
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    network.to(device)
    
translator = AbstractTranslator(abducibles, exclusive)
dataManager = Operator2x2Manager()
outputClasses = [10] * 4
outputClasses.extend([3] * 4)
evaluator = Evaluator()
scenario = 'operator2x2'
model_name = 'model_samples_3000_iter_200_epoch_1.mdl'

scenario_test(network, outputClasses, translator, dataManager, scenario, model_name, evaluator)
