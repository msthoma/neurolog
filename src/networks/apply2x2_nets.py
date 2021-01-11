
import torch
import torch.nn as nn
from typing import List

class COMP_NET(nn.Module):
    def __init__(self):
        super(COMP_NET, self).__init__()
        self.encoder = nn.Sequential(
            nn.Conv2d(1, 6, 5),
            nn.MaxPool2d(2, 2), # 6 24 24 -> 6 12 12
            nn.ReLU(True),
            nn.Conv2d(6, 16, 5), # 6 12 12 -> 16 8 8
            nn.MaxPool2d(2, 2), # 16 8 8 -> 16 4 4
            nn.ReLU(True)
        )
        self.classifier =  nn.Sequential(
            nn.Linear(16 * 5 * 5, 120),
            nn.ReLU(),
            nn.Linear(120, 84),
            nn.ReLU(),
            nn.Linear(84, 3),
            nn.Softmax(1)
        )
        
    def forward(self, vector:List):
        outputs = list()
        for x in vector:
            x = self.encoder(x)
            x = x.view(-1, 16 * 5 * 5)
            x = self.classifier(x)
            outputs.append(x)
        tensor = torch.cat(outputs, 1)
        return tensor    

