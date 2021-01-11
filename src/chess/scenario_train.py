

import torch.optim
import os

from networks.mnist_nets import COMP_NET
from chess.chess_translator import ChessTranslator
from train import Trainer
from params import useGPU, number_of_training_examples, learning_rate, nr_epochs, minibatch_size, snapshot_iter, logs_root,\
    data_root, models_root, sicstus_bin
import random
from chess.abduction.chessNGA import ChessAbductionNGA
from chess.managers.chessBSV_NGA import ChessManagerBSV_NGA
from chess.abduction.chessISK import ChessAbductionISK
from chess.abduction.chessBSV import ChessAbductionBSV
from chess.managers.chessISK import ChessManagerISK
from chess.abducibles import abducibles, exclusive 
from chess.local_params import chess

#Choose the right scenario
#case = 'BSV'
#case = 'ISK'
case = 'NGA'

for run in [1,2,3,4,5]:
    translator = ChessTranslator(abducibles, exclusive)
    network = COMP_NET(chess.numberOfPieces())
        
    if useGPU:
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        network.to(device)
                
    if case == 'BSV':
        dataManager = ChessManagerBSV_NGA()
        abduction = ChessAbductionBSV(sicstus_bin, translator,chess)
        neural_guided_abduction = False
    elif case == 'ISK':
        dataManager = ChessManagerISK()
        abduction = ChessAbductionISK(sicstus_bin, translator)
        neural_guided_abduction = False
    elif case == 'NGA':
        dataManager = ChessManagerBSV_NGA()
        abduction = ChessAbductionNGA(sicstus_bin, translator)
        neural_guided_abduction = True

    data = dataManager.loadExampleTuples(data_root + 'chess/train_data.txt')
    
    shuffling_index = 0
    while shuffling_index < 120:
        random.shuffle(data)
        shuffling_index += 1
    examples = data[1:number_of_training_examples]
    
    #Path to store the neural network models
    model_path = models_root + case + '/' + str(run) + '/' 
    if not os.path.exists(model_path):
        os.makedirs(model_path)
        
    logs_path = logs_root + case + '/'
    if not os.path.exists(logs_path):
        os.makedirs(logs_path)
    
    optimizer = torch.optim.Adam(network.parameters(), lr = learning_rate)
    
    trainer = Trainer(network, chess.getOutputClasses(), dataManager, optimizer, translator, abduction, model_path)
    
    trainer.train(examples, nr_epochs= nr_epochs, minibatch_size = minibatch_size, snapshot_iter = snapshot_iter, shuffle = False, neural_guided_abduction = neural_guided_abduction, logs_path = logs_path)




