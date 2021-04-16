import re
from pathlib import Path

import torch

from abducibles import abducibles, exclusive
from evaluate import Evaluator
from local_params import dataset_names, scenario_name
from manager import SmallerThanManager
from src.abstract_translator import AbstractTranslator
from src.networks.mnist_nets import COMP_NET
from src.params import useGPU, models_root
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
    i = 0
    if i:
        scenario_test(network, outputClasses, translator, dataManager, scenario_name, model_name, evaluator,
                      test_dataset="E2.csv", train_dataset="T2")
    train_datasets = [d for d in dataset_names if "T" in d]
    test_datasets = [d for d in dataset_names if "E" in d]

    # evaluate for each of the models trained by the datasets T1 and T2
    for train_dataset in train_datasets:
        path = Path(models_root) / scenario_name / train_dataset
        iter_models = dict()

        # get path of the saved models at every 100 iterations
        for i in sorted(path.glob("*.mdl")):
            # extract iteration number
            n_iter = int(re.search(pattern=r"iter_(\d*)", string=i.name).groups()[0])
            iter_models[n_iter] = i
        print(sorted(iter_models.keys()))
