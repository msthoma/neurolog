import random

from src.datasets import mnist_test_data, mnist_train_data
from src.params import data_root


def createExamples(dataset, number_of_examples, filename):
    random.seed()
    with open(filename, 'w') as f:
        example_index = 0
        while example_index < number_of_examples:
            image1_index = random.randint(0, len(dataset) - 1)
            image2_index = random.randint(0, len(dataset) - 1)
            image3_index = random.randint(0, len(dataset) - 1)
            image4_index = random.randint(0, len(dataset) - 1)
            (_, digit1), (_, digit2), (_, digit3), (_, digit4) = dataset[image1_index], dataset[image2_index], dataset[
                image3_index], dataset[image4_index]
            f.write(
                'digit11_image={},digit12_image={},digit21_image={},digit22_image={},row1_sum={},row2_sum={},col1_sum={},col2_sum={}\n'.format(
                    image1_index, image2_index, image3_index, image4_index, \
                    digit1 + digit2, digit3 + digit4, digit1 + digit3, digit2 + digit4))
            example_index += 1


createExamples(mnist_train_data, 50000, data_root + "add2x2/train_data.txt")
createExamples(mnist_test_data, 100000, data_root + "add2x2/test_data.txt")
