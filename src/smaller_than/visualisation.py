from collections import defaultdict
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from local_params import scenario_name
from src.params import results_root

if __name__ == '__main__':
    # setup plots
    fig, axes = plt.subplots(2, 2, figsize=(10, 10))

    # import result files
    test_results = defaultdict(dict)
    for results_file in sorted((Path(results_root) / scenario_name).glob("*.csv")):
        _, train_dataset, _, test_dataset, _, seed = results_file.stem.split("_")
        with open(results_file, "r") as f:
            dt = pd.read_csv(f, sep=",", index_col="iteration")
            dt.columns = [f"iteration_{seed}"]

            if test_dataset in test_results[train_dataset]:
                test_results[train_dataset][test_dataset] = pd.concat([test_results[train_dataset][test_dataset], dt],
                                                                      axis=1)
            else:
                test_results[train_dataset][test_dataset] = dt

    # plot results
    colors = iter(["b", "g", "r", "k"])
    for i, (train_dataset, test_datasets) in enumerate(test_results.items()):
        for j, (test_dataset, results) in enumerate(test_datasets.items()):
            results = pd.concat([results.median(axis=1), results.min(axis=1), results.max(axis=1)], axis=1)
            results.columns = ["median", "min", "max"]
            color = next(colors)
            x, y = np.array(results.index), np.array(results["median"])
            axes[i, j].set_ylim(50, 102)
            axes[i, j].set_xlim(0, 9500)
            axes[i, j].plot(x, y, color, linewidth=1, label="Median accuracy (%) / iteration")
            axes[i, j].fill_between(x, np.array(results["min"]), np.array(results["max"]),
                                    facecolor=color, alpha=0.3, label="Range of accuracy values")
            if i == 1: axes[i, j].set_xlabel("Iterations", fontsize=12)
            if j == 0: axes[i, j].set_ylabel(f"Trained with {train_dataset}", fontsize=20)
            if i == 0: axes[i, j].set_title(f"Tested with {test_dataset}", fontsize=20)
            axes[i, j].legend(loc='lower right', fontsize=10)
            axes[i, j].tick_params(axis='both', which='major')

    fig.show()
    fig.savefig(Path(results_root) / scenario_name / "accuracy.pdf", format="pdf", bbox_inches="tight")
