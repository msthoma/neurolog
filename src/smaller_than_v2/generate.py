import random
from pathlib import Path

import pandas as pd
from torchvision.datasets.mnist import MNIST

from local_params import dataset_names, scenario_name
from src.datasets import mnist_test_data, mnist_train_data
from src.params import data_root


def create_examples(dataset: MNIST, number_of_examples: int, pair_type: int, filename: Path, random_seed: int = 42):
    """
    Generates datasets for the `smaller_than` scenario.

    :param dataset: the MNIST dataset, either train or test subsets
    :param number_of_examples: the number of pairs in the generated dataset
    :param pair_type: the type of pairs that the dataset will contain; 0: pairs containing either two odd or two even
     digits, and 1: pairs containing exactly one odd and one even digit
    :param filename: the filename of the resulting dataset
    :param random_seed: ..........................
    """
    assert pair_type in [0, 1], "pair_type must be one of [0, 1]"

    random.seed(random_seed)

    # get indices of even and odd digits in the dataset
    even_digit_indices, odd_digit_indices = list(), list()
    for i in range(len(dataset)):
        _, digit = dataset[i]
        if digit % 2 == 0:
            even_digit_indices.append(i)
        else:
            odd_digit_indices.append(i)

    # create pairs
    pairs = list()
    if pair_type == 0:  # two odd or two even digits
        for _ in range(number_of_examples):
            # creates equal numbers of pairs with odd or even numbers
            indices = [even_digit_indices, odd_digit_indices][random.randint(0, 1)]  # pick either even or odd numbers

            i_1, i_2 = random.sample(range(len(indices)), 2)  # two random picks without replacement
            i_1, i_2 = indices[i_1], indices[i_2]  # convert back to dataset indices

            digit_1, digit_2 = dataset[i_1][1], dataset[i_2][1]  # get actual digits
            assert (digit_1 + digit_2) % 2 == 0  # check that the digits are both either even or odd

            pairs.append([i_1, i_2, digit_1, digit_2, digit_1 < digit_2])

    elif pair_type == 1:  # exactly one odd and one even digit
        for _ in range(number_of_examples):
            # pick one even and one odd number
            odd_i = odd_digit_indices[random.randint(0, len(odd_digit_indices) - 1)]
            even_i = even_digit_indices[random.randint(0, len(even_digit_indices) - 1)]

            pair = [odd_i, even_i]
            random.shuffle(pair)  # shuffle pair so that it's not always [odd, even]

            digit_1, digit_2 = dataset[pair[0]][1], dataset[pair[1]][1]  # get actual digits
            assert (digit_1 + digit_2) % 2 == 1  # check that we have one even and one odd digit

            pairs.append([*pair, digit_1, digit_2, digit_1 < digit_2])

    # write dataset to csv file
    dt = pd.DataFrame(pairs, columns=["digit_1_image", "digit_2_image", "digit_1", "digit_2", "label"])

    filename.parent.mkdir(exist_ok=True)  # make sure subdirectory exists

    with open(filename, "w") as f:
        dt.to_csv(f, sep=",", header=False, index=False)


if __name__ == '__main__':
    pair_types = [0, 1, 0, 1]

    for dt_name, p_type in zip(dataset_names, pair_types):
        print(f"Generating {dt_name} dataset...", end=" ", flush=True)
        create_examples(dataset=mnist_train_data if "T" in dt_name else mnist_test_data,
                        number_of_examples=20000 if "T" in dt_name else 5000, pair_type=p_type,
                        filename=Path(data_root) / scenario_name / f"{dt_name}.csv")
        print("Done!", flush=True)
