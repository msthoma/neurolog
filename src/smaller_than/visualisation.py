from collections import defaultdict
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from local_params import scenario_name
from src.params import results_root


def import_data(filename: str):
    x, y = list(), list()
    with open(filename) as fp:
        while True:
            line = fp.readline()
            line = line.rstrip("\n")
            if not line:
                break

            data = line.split(' ')
            x.append(float(data[0]))
            y.append(float(data[1]))

    return np.array(x), np.array(y)


def compute_std(path):
    arrays = []
    for scenario in [1, 2, 3, 4, 5]:
        filename = path + 'accuracy_vs_iter_' + str(scenario) + '.txt'
        (_, y) = import_data(filename)
        arrays.append(y)

    a = np.array([arrays[0], arrays[1], arrays[2], arrays[3], arrays[4]])
    return np.std(a, axis=1)


def create_curves(path):
    arrays = []
    for scenario in [1, 2, 3, 4, 5]:
        filename = path + 'accuracy_vs_iter_' + str(scenario) + '.txt'
        (x, y) = import_data(filename)
        arrays.append(y)

    ymin = arrays[0]
    ymax = arrays[0]

    for index in [1, 2, 3, 4]:
        ymin = np.minimum(ymin, arrays[index])
        ymax = np.maximum(ymax, arrays[index])

    median = []
    for index in range(0, len(ymin)):
        value = np.median([arrays[0][index], arrays[1][index], arrays[2][index], arrays[3][index], arrays[4][index]])
        median.append(value)

    return x, ymin, ymax, np.array(median)


if __name__ == '__main__':
    # BIGGER_SIZE = 16
    #
    # plt.rc('font', size=BIGGER_SIZE)  # controls default text sizes
    # plt.rc('axes', titlesize=BIGGER_SIZE)  # fontsize of the axes title
    # plt.rc('axes', labelsize=BIGGER_SIZE)  # fontsize of the x and y labels
    # plt.rc('xtick', labelsize=BIGGER_SIZE)  # fontsize of the tick labels
    # plt.rc('ytick', labelsize=BIGGER_SIZE)  # fontsize of the tick labels
    # plt.rc('legend', fontsize=BIGGER_SIZE)  # legend fontsize
    # plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title
    #
    # _, ax = plt.subplots()
    # ax.set_xlim(0, 9000)
    # ax.set_ylim(0, 110)
    #
    # path1 = results_root + "BSV/"
    # x, ymin1, ymax1, ymed1 = create_curves(path1)
    #
    # path2 = results_root + "ISK/"
    # x, ymin2, ymax2, ymed2 = create_curves(path2)
    #
    # path3 = results_root + "NGA/"
    # x, ymin3, ymax3, ymed3 = create_curves(path3)
    #
    # line1, = ax.plot(x, ymed1, '-')
    # ax.fill_between(x, ymin1, ymax1, alpha=0.2)
    #
    # line2, = ax.plot(x, ymed2, 'g-')
    # ax.fill_between(x, ymin2, ymax2, facecolor='g', alpha=0.2)
    #
    # line3, = ax.plot(x, ymed3, 'r-')
    # ax.fill_between(x, ymin3, ymax3, facecolor='r', alpha=0.2)
    #
    # plt.legend([line1, line2, line3], ["NLOG ?=BSV n=3", "NLOG ?=ISK n=3", "NLOG ?=NGA n=3"], loc='lower right')
    # plt.savefig('accuracy.png', format='png', bbox_inches='tight')

    fig, axes = plt.subplots(2, 2, figsize=(10, 10))  # , sharex="all", sharey="all")

    # import results files
    evaluation_results = defaultdict(dict)

    for results_file in sorted((Path(results_root) / scenario_name).glob("*.csv")):
        _, train_dataset, _, test_dataset, _ = results_file.stem.split("_")
        with open(results_file, "r") as f:
            evaluation_results[train_dataset][test_dataset] = pd.read_csv(f, sep=",")
    c = 0
    for i, (train_dataset, test_datasets) in enumerate(evaluation_results.items()):
        for j, (test_dataset, results) in enumerate(test_datasets.items()):
            print(i, j, train_dataset, test_dataset)

            x, y = np.array(results["iteration"]), np.array(results["accuracy"])
            axes[i, j].set_ylim(0, 110)
            axes[i, j].set_xlim(0, 9500)
            axes[i, j].plot(x, y, ["b", "g", "r", "y"][c], label="Accuracy % / iteration")
            if i == 1: axes[i, j].set_xlabel("Iterations")
            if j == 0: axes[i, j].set_ylabel(train_dataset, fontsize=20)
            if i == 0: axes[i, j].set_title(test_dataset, fontsize=20)
            axes[i, j].legend(loc='lower right')
            axes[i, j].tick_params(axis='both', which='major')
            c += 1

    plt.show()
    fig.savefig(Path(results_root) / scenario_name / "accuracy.pdf", format="pdf", bbox_inches="tight")
