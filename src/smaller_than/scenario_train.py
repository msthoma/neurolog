import torch

from abducibles import abducibles, exclusive
from abduction import Abduction
from local_params import scenario_name
from manager import SmallerThanManager
from src.abstract_translator import AbstractTranslator
from src.networks.mnist_nets import COMP_NET
from src.params import useGPU, sicstus_bin
from src.run import scenario_train

network = COMP_NET()
if useGPU:
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    network.to(device)

translator = AbstractTranslator(abducibles, exclusive)
dataManager = SmallerThanManager()
abduction = Abduction(sicstus_bin, translator)
outputClasses = [10] * 2

if __name__ == '__main__':
    # Train on T1
    scenario_train(network, outputClasses, translator, dataManager, scenario_name, abduction,
                   dataset_name="T1_dataset.csv")
