
from typing import List
from benchmark_manager import Goal, Example, BenchmarkManager, computeNeuralInput
from datasets import mnist_train_data, mnist_test_data

class DBAGoal(Goal):    
    def __init__(self, label:int):
        Goal.__init__(self, label)

    def __eq__(self, other):
        if not isinstance(other, DBAGoal):
            return NotImplemented
        return self.label == other.label
    
    def __hash__(self):
        return hash(self.label) 
    
    def __str__(self):
        return 'label=' + str(self.label)

class DBAExample(Example):    
    def __init__(self, images:List[int], label:int):
        Example.__init__(self, label)
        self.images = images   
    
    def __str__(self):
        images_str = 'symbol_images=('
        index = 0
        while index < len(self.images):
            images_str += str(self.images[index])
            if index < len(self.images) - 1:
                images_str += ','
            index += 1
        images_str += ')'
        
        return images_str + ',' + 'label=' + str(self.label)

class DBAManager(BenchmarkManager):

    def __init__(self):
        BenchmarkManager.__init__(self)
    
    def parseString(self, line:str)->DBAExample:
        index = line.find(')', 0)
        images_str = line[len("symbol_images=("):index]
        images = images_str.split(',')
        symbols = list()
        for image in images:
            symbols.append(int(image))    

        index = line.find('label=', 0)
        label_str = line[index + len('label='):]
        if label_str == 'True': 
            label = 1 
        else: 
            label = 0 
        return DBAExample(symbols, label)
    
    def computeNeuralInput(self, example:DBAExample, dataset='train'):     
        if dataset == 'train': 
            datasets = [mnist_train_data] * len(example.images)
        else: 
            datasets = [mnist_test_data] * len(example.images)
        return computeNeuralInput(example.images, datasets)
    
    
    def computeGoal(self, example:DBAExample)->Goal:
        return DBAGoal(example.label)
