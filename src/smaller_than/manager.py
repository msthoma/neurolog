from src.benchmark_manager import Goal, Example, BenchmarkManager, computeNeuralInput
from src.datasets import mnist_train_data, mnist_test_data


class SmallerThanGoal(Goal):
    def __init__(self, digit1: int, digit2: int, label: bool):
        Goal.__init__(self, label)
        self.digit1 = digit1
        self.digit2 = digit2

    def __eq__(self, other):
        if not isinstance(other, SmallerThanGoal):
            return NotImplemented
        return self.digit1 == other.digit1 and self.digit2 == other.digit2 and self.label == other.label

    def __hash__(self):
        return hash((self.digit1, self.digit2, self.label))

    def __str__(self):
        return 'digit1=' + str(self.digit1) + ',' + 'digit2=' + str(self.digit2) + ',' + 'label=' + str(self.label)


class SmallerThanExample(Example):
    def __init__(self, digit1: int, digit2: int, digit1_image: int, digit2_image: int, label: bool):
        Example.__init__(self, label)
        self.digit1 = digit1
        self.digit2 = digit2
        self.digit1_image = digit1_image
        self.digit2_image = digit2_image

    def __str__(self):
        return f"digit1={self.digit1},digit2={self.digit2},images={[self.digit1_image, self.digit2_image]},label={self.label}"


class SmallerThanManager(BenchmarkManager):
    def __init__(self):
        BenchmarkManager.__init__(self)

    def parseString(self, line: str) -> SmallerThanExample:
        # 441,4609,0,4,True
        items = line.strip().split(sep=",")
        digit1_image, digit2_image, digit1, digit2 = list(map(int, items[:-1]))
        label = 1 if items[-1] == "True" else 0

        return SmallerThanExample(digit1, digit2, digit1_image, digit2_image, label)

    def computeNeuralInput(self, example: SmallerThanExample, dataset='train'):
        if dataset == 'train':
            datasets = [mnist_train_data] * 2
        else:
            datasets = [mnist_test_data] * 2
        return computeNeuralInput([example.digit1_image, example.digit2_image], datasets)

    def computeGoal(self, example: SmallerThanExample) -> Goal:
        return SmallerThanGoal(example.digit1, example.digit2, example.label)
