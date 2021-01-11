
from typing import List
from torch.autograd import Variable
from params import useGPU

class Goal(object):    
    def __init__(self, label):
        self.label = label
        
    def __hash__(self):
        return hash(self.label) 
    
class Example(object):    
    def __init__(self, label):
        self.label = label
    
    def getLabel(self):
        return self.label
            
class BenchmarkManager(object):
    
    def __init__(self):
        pass
    
    def computeNeuralInput(self, example:Example, dataset):     
        pass
    
    def loadExampleTuples(self, fileName:str)->List[Example]:
        examples = list()
        with open(fileName) as fp:
            while True:
                line = fp.readline()
                line = line.rstrip("\n")
                if not line:
                    break
                if not line.startswith('#'):
                    examples.append(self.parseString(line))
        return examples
    
    def parseString(self, line:str)->Example:
        pass
    
    def computeGoal(self, example:Example)->Goal:
        pass
    
def computeNeuralInput(images:List[int], datasets:List):     
    data = list()
    index = 0
    for image in images:
        d, _ = datasets[index][image]
        if useGPU:
            data.append(Variable(d.unsqueeze(0).cuda()))
        else:
            data.append(Variable(d.unsqueeze(0)))
        index += 1
    if len(images) > 1:
        return data
    else: 
        return data[0]




  

        

    