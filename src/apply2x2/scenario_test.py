import torch

from src.abstract_translator import AbstractTranslator
from src.apply2x2.abducibles import abducibles, exclusive
from src.apply2x2.evaluate import Evaluator
from src.apply2x2.manager import Apply2x2Manager
from src.networks.apply2x2_nets import COMP_NET
from src.params import useGPU
from src.run import scenario_test

network = COMP_NET()
if useGPU:
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    network.to(device)

translator = AbstractTranslator(abducibles, exclusive)
dataManager = Apply2x2Manager()
outputClasses = [3] * 4
evaluator = Evaluator()
scenario = 'apply2x2'
model_name = 'model_samples_3000_iter_100_epoch_1.mdl'

scenario_test(network, outputClasses, translator, dataManager, scenario, model_name, evaluator)
