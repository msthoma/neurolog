import os
import random

import torch.optim

from src.abstract_adbuction import AbstractAbduction
from src.abstract_translator import AbstractTranslator
from src.benchmark_manager import BenchmarkManager
from src.params import data_root, number_of_training_examples, models_root, learning_rate, nr_epochs, minibatch_size, \
    snapshot_iter, shuffle
from src.test import Tester
from src.train import Trainer


def scenario_train(network, outputClasses, translator: AbstractTranslator, dataManager: BenchmarkManager, scenario,
                   abduction: AbstractAbduction, dataset_name: str = None):
    examples = dataManager.loadExampleTuples(
        data_root + scenario + "/" + f"{dataset_name}.csv" if dataset_name is not None else "train_data.txt")

    shuffling_index = 0
    while shuffling_index < 10:
        random.shuffle(examples)
        shuffling_index += 1

    examples = examples[1:number_of_training_examples]
    model_path = models_root + scenario + "/" + f'{dataset_name}/' if dataset_name is not None else ''
    if not os.path.exists(model_path):
        os.makedirs(model_path)

    optimizer = torch.optim.Adam(network.parameters(), lr=learning_rate)
    trainer = Trainer(network, outputClasses, dataManager, optimizer, translator, abduction, model_path)
    trainer.train(examples, nr_epochs=nr_epochs, minibatch_size=minibatch_size, snapshot_iter=snapshot_iter,
                  shuffle=shuffle)


def scenario_test(network, outputClasses, translator: AbstractTranslator, dataManager: BenchmarkManager, scenario,
                  model_name, evaluator, train_dataset: str = None, test_dataset: str = None):
    model_path = models_root + scenario + "/"
    if train_dataset is not None:
        model_path = f"{model_path}{train_dataset}/{model_name}"
    else:
        model_path = f"{model_path}/{model_name}"
    print(model_path)
    network.load_state_dict(torch.load(model_path))
    examples = dataManager.loadExampleTuples(
        data_root + scenario + "/" + test_dataset if test_dataset is not None else "test_data.txt")
    tester = Tester(network, outputClasses, dataManager, translator, evaluator)
    tester.test(examples)
