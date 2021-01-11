
from typing import List
import torch
import torch.nn as nn

from benchmark_manager import BenchmarkManager, Example
from abstract_translator import AbstractTranslator

class Tester(object):
    
    def __init__(self, network:nn.Module, outputClasses:List, benchmarkManager:BenchmarkManager, translator:AbstractTranslator, evaluator):
        self.network = network
        self.benchmarkManager = benchmarkManager
        self.evaluator = evaluator
        self.outputClasses = outputClasses
        self.translator = translator

    def evaluate(self, example:Example)->bool:
        
        nninput = self.benchmarkManager.computeNeuralInput(example, dataset = 'test')
        nnoutput = self.network(nninput)
        
        facts = list()
        start = 0
        for index in range(len(self.outputClasses)):
            _, predicted = torch.max(nnoutput.data[0,start:start + self.outputClasses[index]], 0)
            facts.append(self.translator.toFact(predicted.item() + start))
            start = start + self.outputClasses[index]
                    
        return self.evaluator.evaluate(facts, example)

    def test(self, examples, log_iter = 100)->float:
        self.network.eval()
        accuracy = 0
        with torch.no_grad():
            correct = 0

            indices = list(range(len(examples)))
            iterations = 1
            for index in indices:             
                result = self.evaluate(examples[index])
                correct += result == True
                if iterations % log_iter == 0:
                    accuracy = (correct / iterations) * 100
                    print('Accuracy %: ', accuracy)
                iterations += 1
        return accuracy 