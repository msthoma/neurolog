import re
from pathlib import Path

import torch

from abducibles import abducibles, exclusive
from evaluate import Evaluator
from local_params import dataset_names, scenario_name
from manager import SmallerThanManager
from src.abstract_translator import AbstractTranslator
from src.networks.mnist_nets import COMP_NET
from src.params import useGPU, models_root, results_root
from src.run import scenario_test

network = COMP_NET()
if useGPU:
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    network.to(device)

translator = AbstractTranslator(abducibles, exclusive)
dataManager = SmallerThanManager()
outputClasses = [10] * 2
evaluator = Evaluator()

if __name__ == '__main__':
    # get train and test dataset names
    train_datasets = [d for d in dataset_names if "T" in d]
    test_datasets = [d for d in dataset_names if "E" in d]

    # evaluate for each of the models trained by the datasets T1 and T2
    for train_dataset in train_datasets:
        models_path = Path(models_root) / scenario_name / train_dataset
        iter_models = dict()

        # get path of the saved models at every 100 iterations
        for iter_model in sorted(models_path.glob("*.mdl")):
            # extract iteration number
            n_iter = int(re.search(pattern=r"iter_(\d*)", string=iter_model.name).groups()[0])
            iter_models[n_iter] = iter_model

        # evaluate model at each iteration (the models are sorted according to their iteration number)
        accuracies = list()
        for n_iter in sorted(iter_models.keys()):
            model_name = iter_models[n_iter].name
            accuracy = scenario_test(network, outputClasses, translator, dataManager, scenario_name, model_name,
                                     evaluator, test_dataset="E2.csv", train_dataset=train_dataset)
            accuracies.append([n_iter, accuracy])

        results_path = Path(results_root) / scenario_name
        results_path.mkdir(exist_ok=True)

        with open(results_path / f"train_{train_dataset}_eval_E2_results", "w") as f:
            for line in accuracies:
                f.write(",".join(map(str, line)) + "\n")
