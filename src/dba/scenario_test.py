
import torch
from networks.mnist_nets import COMP_NET
from abstract_translator import AbstractTranslator
from dba.manager import DBAManager
from dba.evaluate import Evaluator
from dba.local_params import number_of_symbols
from params import useGPU
from run import scenario_test
from dba.abducibles import abducibles, exclusive

network = COMP_NET(4)
if useGPU:
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    network.to(device)

translator = AbstractTranslator(abducibles, exclusive)
dataManager = DBAManager()
outputClasses = [4] * number_of_symbols  
evaluator = Evaluator(number_of_symbols)
scenario = 'dba/' + str(number_of_symbols)
model_name = 'model_samples_3000_iter_500_epoch_1.mdl'

scenario_test(network, outputClasses, translator, dataManager, scenario, model_name, evaluator)
