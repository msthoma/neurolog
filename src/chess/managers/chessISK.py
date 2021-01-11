
from typing import List
from benchmark_manager import Goal, Example, BenchmarkManager, computeNeuralInput
from datasets import mnist_train_data, mnist_test_data

class ChessGoal(Goal):    
    def __init__(self, coordinates:List, label:str):
        Goal.__init__(self, label)
        self.coordinates = coordinates   
        
    def __eq__(self, other):
        if not isinstance(other, ChessGoal):
            return NotImplemented
        return self.coordinates == other.coordinates and self.label == other.label
    
    def __hash__(self):
        return hash((str(self.coordinates), self.label)) 
    
    def __str__(self):
        return 'coordinates=' + str(self.coordinates) + ',label=' + str(self.label)
    
class ChessExample(Example):    
    def __init__(self, images:List[int], coordinates:List, label:bool):
        Example.__init__(self, label)
        self.images = images   
        self.coordinates = coordinates   
        
class ChessManagerISK(BenchmarkManager):

    def __init__(self):
        BenchmarkManager.__init__(self)
        
    def parseString(self, line:str)->ChessExample:
        index = line.find(')', 0)
        images_str = line[len("digit_images=("):index]
        images = images_str.split(',')
        data = list()
        for image in images:
            data.append(int(image))    
            
        index1 = line.find('coordinates=(', 0)
        index2 = line.find('),label', 0)
        coordinates_str = line[index1 + len('coordinates=('):index2]
        coordinates_str = coordinates_str.split(',')
        coordinates = list()
        for coordinate in coordinates_str: 
            x = int(coordinate[1])
            y = int(coordinate[3])
            coordinates.append((x,y))
        index = line.find('label=', 0)
        label_str = line[index + len('label='):]
        return ChessExample(data, coordinates, label_str)
    
    def computeNeuralInput(self, example:ChessExample, dataset = 'train'):    
        if dataset == 'train': 
            datasets = [mnist_train_data] * len(example.images)
        else: 
            datasets = [mnist_test_data] * len(example.images)
        return computeNeuralInput(example.images, datasets)
    
    def computeGoal(self, example:ChessExample)->Goal:
        return ChessGoal(example.coordinates, example.label)