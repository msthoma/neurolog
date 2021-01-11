
from typing import List
from benchmark_manager import Goal, Example, BenchmarkManager, computeNeuralInput
from datasets import mnist_train_data, mnist_test_data, hasy_test_data, hasy_train_data

class MathGoal(Goal):    
    def __init__(self, label:int):
        Goal.__init__(self, label)

    def __eq__(self, other):
        if not isinstance(other, MathGoal):
            return NotImplemented
        return self.label == other.label
    
    def __hash__(self):
        return hash(self.label) 
    
    def __str__(self):
        return 'label=' + str(self.label)

class MathExample(Example):    
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
        return images_str + ',' +'label=' + str(self.label)

class MathManager(BenchmarkManager):

    def __init__(self):
        BenchmarkManager.__init__(self)
    
    def parseString(self, line:str)->MathExample:
        index = line.find(')', 0)
        images_str = line[len("symbol_images=("):index]
        images = images_str.split(',')
        data = list()
        for image in images:
            data.append(int(image))    
        index1 = line.find('label=', 0)
        label_str = line[index1 + len('label='):]
        label = int(label_str)
        return MathExample(data, label)
    
    def computeNeuralInput(self, example:MathExample, dataset='train'):     
        datasets = list()
        index = 0
        if dataset == 'train': 
            while index < len(example.images):
                if index % 2 == 0:
                    datasets.append(mnist_train_data)
                else:
                    datasets.append(hasy_train_data)
                index += 1
        else: 
            while index < len(example.images):
                if index % 2 == 0:
                    datasets.append(mnist_test_data)
                else:
                    datasets.append(hasy_test_data)
                index += 1
        return computeNeuralInput(example.images, datasets)
    
    def computeGoal(self, example:MathExample)->Goal:
        return MathGoal(example.label)
