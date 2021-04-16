import matplotlib.pyplot as plt
import numpy as np

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
    BIGGER_SIZE = 16

    plt.rc('font', size=BIGGER_SIZE)  # controls default text sizes
    plt.rc('axes', titlesize=BIGGER_SIZE)  # fontsize of the axes title
    plt.rc('axes', labelsize=BIGGER_SIZE)  # fontsize of the x and y labels
    plt.rc('xtick', labelsize=BIGGER_SIZE)  # fontsize of the tick labels
    plt.rc('ytick', labelsize=BIGGER_SIZE)  # fontsize of the tick labels
    plt.rc('legend', fontsize=BIGGER_SIZE)  # legend fontsize
    plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title

    _, ax = plt.subplots()
    ax.set_xlim(0, 9000)
    ax.set_ylim(0, 110)

    path1 = results_root + "BSV/"
    x, ymin1, ymax1, ymed1 = create_curves(path1)

    path2 = results_root + "ISK/"
    x, ymin2, ymax2, ymed2 = create_curves(path2)

    path3 = results_root + "NGA/"
    x, ymin3, ymax3, ymed3 = create_curves(path3)

    line1, = ax.plot(x, ymed1, '-')
    ax.fill_between(x, ymin1, ymax1, alpha=0.2)

    line2, = ax.plot(x, ymed2, 'g-')
    ax.fill_between(x, ymin2, ymax2, facecolor='g', alpha=0.2)

    line3, = ax.plot(x, ymed3, 'r-')
    ax.fill_between(x, ymin3, ymax3, facecolor='r', alpha=0.2)

    plt.legend([line1, line2, line3], ["NLOG ?=BSV n=3", "NLOG ?=ISK n=3", "NLOG ?=NGA n=3"], loc='lower right')
    plt.savefig('accuracy.png', format='png', bbox_inches='tight')
