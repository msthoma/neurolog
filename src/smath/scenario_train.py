import torch

from src.abstract_translator import AbstractTranslator
from src.networks.symbols_math_nets import COMP_NET
from src.params import useGPU, sicstus_bin
from src.run import scenario_train
from src.smath.abducibles import abducibles, exclusive
from src.smath.abduction import Abduction
from src.smath.local_params import number_of_symbols
from src.smath.manager import MathManager

network = COMP_NET()
if useGPU:
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    network.to(device)

translator = AbstractTranslator(abducibles, exclusive)
dataManager = MathManager()
abduction = Abduction(sicstus_bin, translator)
outputClasses = list()
index = 1
while index <= number_of_symbols:
    if index % 2 != 0:
        outputClasses.append(10)
    else:
        outputClasses.append(3)
    index += 1
scenario = 'math/' + str(number_of_symbols)

scenario_train(network, outputClasses, translator, dataManager, scenario, abduction)
