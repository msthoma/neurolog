
from typing import List
from benchmark_manager import Goal, Example, BenchmarkManager, computeNeuralInput
from datasets import mnist_test_data, mnist_train_data
import torch

class Opereator2x2Goal(Goal):    
    def __init__(self, label:List):
        Goal.__init__(self, label)

    def __eq__(self, other):
        if not isinstance(other, Opereator2x2Goal):
            return NotImplemented
        return self.label == other.label
    
    def __hash__(self):
        return hash((self.label[0], self.label[1], self.label[2], self.label[3]))
    
    def __str__(self):
        return 'label=' + str(self.label)

class Operator2x2Example(Example):    
    def __init__(self, digit11_image:int, digit12_image:int, digit21_image:int, digit22_image:int, label:List):
        Example.__init__(self, label)
        self.digit11_image = digit11_image
        self.digit12_image = digit12_image
        self.digit21_image = digit21_image
        self.digit22_image = digit22_image
    
    def __str__(self):
        return 'digit11_image=' + str(self.digit11_image) + ',' + 'digit12_image=' + str(self.digit12_image) + ',' + \
        'digit21_image=' + str(self.digit21_image) + ',' + 'digit22_image=' + str(self.digit22_image) + ',label=' + str(self.label)

class Operator2x2Manager(BenchmarkManager):

    def __init__(self):
        BenchmarkManager.__init__(self)
    
    def parseString(self, line:str)->Operator2x2Example:
        index1 = line.find('digit11_image=', 0)
        index2 = line.find(',digit12_image=', 0)
        digit11_str = line[index1 + len('digit11_image='):index2]
        digit11 = int(digit11_str)
        
        index1 = line.find('digit12_image=', 0)
        index2 = line.find(',digit21_image=', 0)
        digit12_str = line[index1 + len('digit12_image='):index2]
        digit12 = int(digit12_str)
        
        
        index1 = line.find('digit21_image=', 0)
        index2 = line.find(',digit22_image=', 0)
        digit21_str = line[index1 + len('digit21_image='):index2]
        digit21 = int(digit21_str)
        
        index1 = line.find('digit22_image=', 0)
        index2 = line.find(',row1_result=', 0)
        digit22_str = line[index1 + len('digit22_image='):index2]
        digit22 = int(digit22_str)
        
        index1 = line.find('row1_result=', 0)
        index2 = line.find(',row2_result=', 0)
        row1_str = line[index1 + len('row1_result='):index2]
        row1 = int(row1_str)
        
        index1 = line.find('row2_result=', 0)
        index2 = line.find(',col1_result=', 0)
        row2_str = line[index1 + len('row2_result='):index2]
        row2 = int(row2_str)
        
        index1 = line.find('col1_result=', 0)
        index2 = line.find(',col2_result=', 0)
        col1_str = line[index1 + len('col1_result='):index2]
        col1 = int(col1_str)
        
        index = line.find('col2_result=', 0)
        col2_str = line[index + len('col2_result='):]
        col2 = int(col2_str)

        return Operator2x2Example(digit11, digit12, digit21, digit22, [row1, row2, col1, col2])
      
    def computeNeuralInput(self, example:Operator2x2Example, dataset='train'):     
        if dataset == 'train': 
            datasets = [mnist_train_data] * 4
        else: 
            datasets = [mnist_test_data] * 4
        images = computeNeuralInput([example.digit11_image, example.digit12_image, example.digit21_image, example.digit22_image], datasets)
        images.extend([torch.zeros(1, 1).cuda(), torch.zeros(1, 1).cuda(), torch.zeros(1, 1).cuda(), torch.zeros(1, 1).cuda()])
        return images 
        
    def computeGoal(self, example:Operator2x2Example)->Goal:
        return Opereator2x2Goal(example.label)
    
    