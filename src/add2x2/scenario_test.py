import torch

from src.abstract_translator import AbstractTranslator
from src.add2x2.abducibles import abducibles, exclusive
from src.add2x2.evaluate import Evaluator
from src.add2x2.manager import Add2x2Manager
from src.networks.mnist_nets import COMP_NET
from src.params import useGPU
from src.run import scenario_test

network = COMP_NET()
if useGPU:
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    network.to(device)

translator = AbstractTranslator(abducibles, exclusive)
dataManager = Add2x2Manager()
outputClasses = [10] * 4
evaluator = Evaluator()
scenario = 'add2x2'
model_name = 'model_samples_3000_iter_9001_epoch_3.mdl'

if __name__ == '__main__':
    scenario_test(network, outputClasses, translator, dataManager, scenario, model_name, evaluator)
