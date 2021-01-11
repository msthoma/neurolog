

import torch
import os
from os import path
from networks.mnist_nets import COMP_NET
from chess.evaluation.chessBSV_NGA import ChessBSV_NGA
from chess.evaluation.chessISK import ChessISK
from test import Tester
from params import useGPU, results_root, data_root, models_root, number_of_training_examples, nr_epochs
import random
from chess.managers.chessBSV_NGA import ChessManagerBSV_NGA
from chess.managers.chessISK import ChessManagerISK
from chess.abducibles import abducibles, exclusive 
from chess.chess_translator import ChessTranslator
from chess.local_params import chess

#Choose the right scenario
#case = 'BSV'
case = 'ISK'
#case = 'NGA'

print("Starting " + os.path.basename(__file__))
random.seed()

filepath = results_root + case + '/'
if not os.path.exists(filepath):
    os.makedirs(filepath)
    
for run in [1,2,3,4,5]:
    translator = ChessTranslator(abducibles, exclusive)
    filename_iter = filepath + 'accuracy_vs_iter_' + str(run) + '.txt'

    if case == 'BSV':
        dataManager = ChessManagerBSV_NGA()
        evaluator = ChessBSV_NGA(chess)
    elif case == 'ISK':
        dataManager = ChessManagerISK()
        evaluator = ChessISK(chess)
    elif case == 'NGA':
        dataManager = ChessManagerBSV_NGA()
        evaluator = ChessBSV_NGA(chess)
    
    data = dataManager.loadExampleTuples(data_root + 'chess/test_data.txt')
    
    shuffling_index = 0
    while shuffling_index < 50:
        random.shuffle(data)
        shuffling_index += 1

    examples = data[1:1500]
    iteration = 200
    epoch = 1

    with open(filename_iter,'w') as f_iter:
    
        while iteration <= nr_epochs * (number_of_training_examples - 1):
             
            network = COMP_NET(chess.numberOfPieces())
            
            if useGPU:
                device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
                network.to(device)
                
            #Path to store the neural network models
            model_path = models_root + case + '/' + str(run) + '/model_samples_' + str(number_of_training_examples - 1) + '_iter_' + str(iteration) + '_epoch_' + str(epoch) + '.mdl'
            if not path.exists(model_path): 
                epoch += 1
                model_path = models_root + case + '/' + str(run) + '/model_samples_' + str(number_of_training_examples - 1) + '_iter_' + str(iteration) + '_epoch_' + str(epoch) + '.mdl' 
            
            print(model_path)
                   
            #Load the nn
            network.load_state_dict(torch.load(model_path))
            
            tester = Tester(network, chess.getOutputClasses(), dataManager, translator, evaluator)

            accuracy = tester.test(examples)
                
            f_iter.write('{} {}\n'.format(iteration, accuracy))    
    
            iteration += 200


