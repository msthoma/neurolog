import random

from torchvision.datasets.mnist import MNIST

from src.datasets import mnist_test_data, mnist_train_data
from src.params import data_root


def create_examples(dataset: MNIST, number_of_examples: int, pair_type: int, filename: str):
    """
    Generates datasets for the `smaller_than` scenario.

    :param dataset: the MNIST dataset, either train or test subsets
    :param number_of_examples: the number of pairs in the generated dataset
    :param pair_type: the type of pairs that the dataset will contain; 0: pairs containing either two odd or two even
     digits, and 1: pairs containing exactly one odd and one even digit
    :param filename: the filename of the resulting dataset
    """
    assert pair_type in [0, 1], "pair_type must be one of [0, 1]"

    random.seed(42)

    # get indices of even and odd digits in the dataset
    even_digit_indices, odd_digit_indices = list(), list()
    for i in range(len(dataset)):
        _, digit = dataset[i]
        if digit % 2 == 0:
            even_digit_indices.append(i)
        else:
            odd_digit_indices.append(i)

    pairs = list()
    if pair_type == 0:  # two odd or two even digits
        for _ in range(number_of_examples):
            # creates equal numbers of pairs with odd or even numbers
            indices = [even_digit_indices, odd_digit_indices][random.randint(0, 1)]  # pick either even or odd numbers

            i_1, i_2 = random.sample(range(len(indices)), 2)  # two random picks without replacement
            i_1, i_2 = indices[i_1], indices[i_2]  # convert back to dataset indices

            digit_1, digit_2 = dataset[i_1][1], dataset[i_2][1]  # get actual digits
            assert (digit_1 + digit_2) % 2 == 0  # check that the digits are both either even or odd

            pairs.append([i_1, i_2, digit_1 < digit_2])

    elif pair_type == 1:  # exactly one odd and one even digit
        for _ in range(number_of_examples):
            # pick one even and one odd number
            odd_i = odd_digit_indices[random.randint(0, len(odd_digit_indices) - 1)]
            even_i = even_digit_indices[random.randint(0, len(even_digit_indices) - 1)]

            pair = [odd_i, even_i]
            random.shuffle(pair)  # shuffle pair so that it's not always [odd, even]

            digit_1, digit_2 = dataset[pair[0]][1], dataset[pair[1]][1]  # get actual digits
            assert (digit_1 + digit_2) % 2 == 1  # check that we have one even and one odd digit

            pairs.append([*pair, digit_1 < digit_2])

    print(sum(d[2] for d in pairs), len(pairs), pair_type)


if __name__ == '__main__':
    create_examples(dataset=mnist_test_data, number_of_examples=1000, pair_type=1,
                    filename=data_root + "smaller_than/train_data.txt")
