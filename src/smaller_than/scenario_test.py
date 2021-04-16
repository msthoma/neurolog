import torch

from abducibles import abducibles, exclusive
from evaluate import Evaluator
from local_params import scenario_name
from manager import SmallerThanManager
from src.abstract_translator import AbstractTranslator
from src.networks.mnist_nets import COMP_NET
from src.params import useGPU
from src.run import scenario_test

network = COMP_NET()
if useGPU:
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    network.to(device)

translator = AbstractTranslator(abducibles, exclusive)
dataManager = SmallerThanManager()
outputClasses = [10] * 2
evaluator = Evaluator()
model_name = 'model_samples_3000_iter_9000_epoch_3.mdl'

if __name__ == '__main__':
    scenario_test(network, outputClasses, translator, dataManager, scenario_name, model_name, evaluator,
                  dataset_name="E1_dataset.csv")
