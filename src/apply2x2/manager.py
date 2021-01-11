from typing import List
from benchmark_manager import Goal, Example, BenchmarkManager, computeNeuralInput
from datasets import hasy_test_data, hasy_train_data

class Apply2x2Goal(Goal):
    def __init__(self, digit1:int, digit2:int, digit3:int, label:List):
        Goal.__init__(self, label)
        self.digit1 = digit1
        self.digit2 = digit2
        self.digit3 = digit3

    def __eq__(self, other):
        if not isinstance(other, Apply2x2Goal):
            return NotImplemented
        return self.digit1 == other.digit1 and self.digit2 == other.digit2 and self.digit3 == other.digit3 and self.label == other.label

    def __hash__(self):
        return hash((self.digit1, self.digit2, self.digit3, self.label[0], self.label[1], self.label[2], self.label[3]))

    def __str__(self):
        return 'digit1=' + str(self.digit1) + ',' + 'digit2=' + str(self.digit2) + ',' + 'digit3=' + str(self.digit3) + ',' + 'label=' + str(self.label)

class Apply2x2Example(Example):
    def __init__(self, digit1:int, digit2:int, digit3:int, op11_image:int, op12_image:int, op21_image:int, op22_image:int, label:List):
        Example.__init__(self, label)
        self.digit1 = digit1
        self.digit2 = digit2
        self.digit3 = digit3
        self.op11_image = op11_image
        self.op12_image = op12_image
        self.op21_image = op21_image
        self.op22_image = op22_image

    def __str__(self):
        return 'digit1=' + str(self.digit1) + ',' + 'digit2=' + str(self.digit2) + ',' + 'digit3=' + str(self.digit3) + ',' + \
        'op11_image=' + str(self.op11_image) + ',' + 'op12_image=' + str(self.op12_image) + ',' + \
        'op21_image=' + str(self.op21_image) + ',' + 'op22_image=' + str(self.op22_image) + ',label=' + str(self.label)

class Apply2x2Manager(BenchmarkManager):

    def __init__(self):
        BenchmarkManager.__init__(self)

    def parseString(self, line:str)->Apply2x2Example:
        index1 = line.find('digit1=', 0)
        index2 = line.find(',digit2=', 0)
        digit1_str = line[index1 + len('digit1='):index2]
        digit1 = int(digit1_str)

        index1 = line.find('digit2=', 0)
        index2 = line.find(',digit3=', 0)
        digit2_str = line[index1 + len('digit2='):index2]
        digit2 = int(digit2_str)

        index1 = line.find('digit3=', 0)
        index2 = line.find(',op11_image=', 0)
        digit3_str = line[index1 + len('digit3='):index2]
        digit3 = int(digit3_str)

        index1 = line.find('op11_image=', 0)
        index2 = line.find(',op12_image=', 0)
        op11_str = line[index1 + len('op11_image='):index2]
        op11_image = int(op11_str)

        index1 = line.find('op12_image=', 0)
        index2 = line.find(',op21_image=', 0)
        op12_str = line[index1 + len('op12_image='):index2]
        op12_image = int(op12_str)

        index1 = line.find('op21_image=', 0)
        index2 = line.find(',op22_image=', 0)
        op21_str = line[index1 + len('op21_image='):index2]
        op21_image = int(op21_str)

        index1 = line.find('op22_image=', 0)
        index2 = line.find(',row1_result=', 0)
        op22_str = line[index1 + len('op22_image='):index2]
        op22_image = int(op22_str)

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

        return Apply2x2Example(digit1, digit2, digit3, op11_image, op12_image, op21_image, op22_image, [row1, row2, col1, col2])

    def computeNeuralInput(self, example:Apply2x2Example, dataset='train'):
        if dataset == 'train':
            datasets = [hasy_train_data] * 4
        else:
            datasets = [hasy_test_data] * 4
        return computeNeuralInput([example.op11_image, example.op12_image, example.op21_image, example.op22_image], datasets)

    def computeGoal(self, example:Apply2x2Example)->Goal:
        return Apply2x2Goal(example.digit1, example.digit2, example.digit3, example.label)

