from typing import List

from src.benchmark_manager import Goal, Example, BenchmarkManager, \
    computeNeuralInput
from src.datasets import mnist_train_data, mnist_test_data


class MemberGoal(Goal):
    def __init__(self, target, label: bool):
        Goal.__init__(self, label)
        self.target = target

    def __eq__(self, other):
        if not isinstance(other, MemberGoal):
            return NotImplemented
        return self.label == other.label and self.target == other.target

    def __hash__(self):
        return hash((self.label, self.target))

    def __str__(self):
        return 'target=' + str(self.target) + ',label=' + str(self.label)


class MemberExample(Example):
    def __init__(self, images: List[int], target: int, label: bool):
        Example.__init__(self, label)
        self.images = images
        self.target = target


class MemberManager(BenchmarkManager):

    def __init__(self):
        BenchmarkManager.__init__(self)

    def parseString(self, line: str) -> MemberExample:
        index = line.find(')', 0)
        images_str = line[len("digit_images=("):index]
        images = images_str.split(',')
        data = list()
        for image in images:
            data.append(int(image))

        index1 = line.find('target=', 0)
        index2 = line.find(',label=', 0)
        target_str = line[index1 + len('target='):index2]
        target = int(target_str)

        index = line.find('label=', 0)
        label_str = line[index + len('label='):]
        if label_str == 'True':
            label = 1
        else:
            label = 0
        return MemberExample(data, target, label)

    def computeNeuralInput(self, example: MemberExample, dataset='train'):
        if dataset == 'train':
            datasets = [mnist_train_data] * len(example.images)
        else:
            datasets = [mnist_test_data] * len(example.images)
        return computeNeuralInput(example.images, datasets)

    def computeGoal(self, example: MemberExample) -> Goal:
        return MemberGoal(example.target, example.label)
