from typing import List

import torch
import torch.nn as nn


class COMP_NET(nn.Module):
    def __init__(self):
        super(COMP_NET, self).__init__()
        self.encoder_mnist = nn.Sequential(
            nn.Conv2d(1, 6, 5),
            nn.MaxPool2d(2, 2),  # 6 24 24 -> 6 12 12
            nn.ReLU(True),
            nn.Conv2d(6, 16, 5),  # 6 12 12 -> 16 8 8
            nn.MaxPool2d(2, 2),  # 16 8 8 -> 16 4 4
            nn.ReLU(True)
        )
        self.classifier_mnist = nn.Sequential(
            nn.Linear(16 * 4 * 4, 120),
            nn.ReLU(),
            nn.Linear(120, 84),
            nn.ReLU(),
            nn.Linear(84, 10),
            nn.Softmax(1)
        )

        self.classifier_op1 = nn.Sequential(
            nn.Linear(1, 120),
            nn.ReLU(),
            nn.Linear(120, 84),
            nn.ReLU(),
            nn.Linear(84, 3),
            nn.Softmax(1)
        )

        self.classifier_op2 = nn.Sequential(
            nn.Linear(1, 120),
            nn.ReLU(),
            nn.Linear(120, 84),
            nn.ReLU(),
            nn.Linear(84, 3),
            nn.Softmax(1)
        )

        self.classifier_op3 = nn.Sequential(
            nn.Linear(1, 120),
            nn.ReLU(),
            nn.Linear(120, 84),
            nn.ReLU(),
            nn.Linear(84, 3),
            nn.Softmax(1)
        )

        self.classifier_op4 = nn.Sequential(
            nn.Linear(1, 120),
            nn.ReLU(),
            nn.Linear(120, 84),
            nn.ReLU(),
            nn.Linear(84, 3),
            nn.Softmax(1)
        )

    def forward(self, vector: List):

        index = 0
        outputs = list()
        while index < len(vector):
            if index < 4:
                x = self.encoder_mnist(vector[index])
                x = x.view(-1, 16 * 4 * 4)
                x = self.classifier_mnist(x)
                outputs.append(x)
            index += 1

        y1 = self.classifier_op1(vector[4])
        outputs.append(y1)

        y2 = self.classifier_op2(vector[5])
        outputs.append(y2)

        y3 = self.classifier_op3(vector[6])
        outputs.append(y3)

        y4 = self.classifier_op4(vector[7])
        outputs.append(y4)

        tensor = torch.cat(outputs, 1)
        return tensor
