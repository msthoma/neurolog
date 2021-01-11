
import torch.optim
import os
from train import Trainer
from test import Tester
from params import data_root, number_of_training_examples, models_root, learning_rate, nr_epochs, minibatch_size, snapshot_iter, shuffle
import random
from abstract_translator import AbstractTranslator
from benchmark_manager import BenchmarkManager
from abstract_adbuction import AbstractAbduction

def scenario_train(network, outputClasses, translator:AbstractTranslator, dataManager:BenchmarkManager, scenario, abduction:AbstractAbduction):

    examples = dataManager.loadExampleTuples(data_root + scenario + '/train_data.txt')
    
    shuffling_index = 0
    while shuffling_index < 10:
        random.shuffle(examples)
        shuffling_index += 1
    
    examples = examples[1:number_of_training_examples]        
    model_path = models_root + scenario + '/'  
    if not os.path.exists(model_path):
        os.makedirs(model_path)
                
    optimizer = torch.optim.Adam(network.parameters(), lr = learning_rate)
    trainer = Trainer(network, outputClasses, dataManager, optimizer, translator, abduction, model_path)
    trainer.train(examples, nr_epochs= nr_epochs, minibatch_size = minibatch_size, snapshot_iter = snapshot_iter, shuffle = shuffle)

def scenario_test(network, outputClasses, translator:AbstractTranslator, dataManager:BenchmarkManager, scenario, model_name, evaluator):

    model_path = models_root + scenario + '/' + model_name
    network.load_state_dict(torch.load(model_path))
    examples = dataManager.loadExampleTuples(data_root + scenario + '/test_data.txt')
    tester = Tester(network, outputClasses, dataManager, translator, evaluator)
    tester.test(examples)