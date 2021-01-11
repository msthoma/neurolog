
import torch
from networks.symbols_math_nets import COMP_NET
from abstract_translator import AbstractTranslator
from smath.manager import MathManager
from smath.evaluate import Evaluator
from smath.local_params import number_of_symbols
from smath.abducibles import abducibles, exclusive  
from run import scenario_test
from params import useGPU

network = COMP_NET()
if useGPU:
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    network.to(device)
translator = AbstractTranslator(abducibles, exclusive)
dataManager = MathManager()
outputClasses = list()
index = 1
while index <= number_of_symbols:
    if index % 2 != 0:
        outputClasses.append(10)
    else: 
        outputClasses.append(3)
    index += 1     
evaluator = Evaluator()
scenario = 'math/' + str(number_of_symbols)
model_name = 'model_samples_3000_iter_100_epoch_1.mdl'

scenario_test(network, outputClasses, translator, dataManager, scenario, model_name, evaluator)


