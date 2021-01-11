
from datasets import mnist_test_data, mnist_train_data
from params import data_root
from chess.local_params import chess
import random
from chess.utilities import convertProofsToTuples

def createExamples(dataset, chess, number_of_mate_cases, number_of_draw_cases, number_of_safe_cases, 
                   examples_per_mate_case, examples_per_draw_case, examples_per_safe_case, 
                   filename:str):
    random.seed()
    
    mate = convertProofsToTuples(chess.getMateProofs())
    draw = convertProofsToTuples(chess.getDrawProofs())
    safe = convertProofsToTuples(chess.getSafeProofs())
    
    dataset_indices = list(range(len(dataset)))
    image_indices_dict = dict()
    for image_id in dataset_indices:
        (_, sign) = dataset[image_id]
        if sign not in image_indices_dict:
            image_indices_dict[sign] = list()
        image_indices_dict[sign].append(image_id)
    
    grid = [(1,1),(1,2),(1,3),(2,1),(2,2),(2,3),(3,1),(3,2),(3,3)]
    
    configurations = [mate, draw, safe]
    games = ['mate', 'draw', 'safe']
    number_of_cases_per_configuration = [number_of_mate_cases, number_of_draw_cases, number_of_safe_cases]
    number_of_examples_per_case = [examples_per_mate_case, examples_per_draw_case, examples_per_safe_case]
    
    with open(filename,'w') as f:
        case = 0
        while case < 3:
            configuration = configurations[case]
            n = number_of_cases_per_configuration[case]
            e = number_of_examples_per_case[case]
            game = games[case]
            
            i = 0
            while i < n:
                (W1,X1,Y1,W2,X2,Y2,X3,Y3) = configuration[i]
                j = 0
                while j < e:
                    g = 0
                    f.write('digit_images=(')
                    while g < len(grid):
                        (X0,Y0) = grid[g]
                        
                        if X0 == X1 and Y0 == Y1:
                            image_ids = image_indices_dict[chess.getPosition(W1)]
                            random_index = random.randint(0, len(image_ids) - 1) 
                            image = image_ids[random_index]
                        elif X0 == X2 and Y0 == Y2:
                            image_ids = image_indices_dict[chess.getPosition(W2)]
                            random_index = random.randint(0, len(image_ids) - 1) 
                            image = image_ids[random_index]
                        elif X0 == X3 and Y0 == Y3:
                            image_ids = image_indices_dict[chess.getBlackKingPosition()]
                            random_index = random.randint(0, len(image_ids) - 1) 
                            image = image_ids[random_index] 
                        else:
                            image_ids = image_indices_dict[chess.getEmptyPosition()]
                            random_index = random.randint(0, len(image_ids) - 1) 
                            image = image_ids[random_index]
                        f.write('{}'.format(image))    
                        if g < len(grid) - 1:
                            f.write(',') 
                        g += 1
                    f.write('),')  
                    
                    f.write('coordinates=(')
                    f.write('({} {}),'.format(X1,Y1))    
                    f.write('({} {}),'.format(X2,Y2))    
                    f.write('({} {})'.format(X3,Y3))    
                    f.write('),')
                      
                    f.write('label={}\n'.format(game))    

                    f.write('#')  
                    f.write('digit_images=(')  
                    g = 0
                    while g < len(grid):
                        (X0,Y0) = grid[g]
                        if X0 == X1 and Y0 == Y1:
                            f.write('({},{},{})'.format(X0,Y0,W1))    
                        elif X0 == X2 and Y0 == Y2:
                            f.write('({},{},{})'.format(X0,Y0,W2))    
                        elif X0 == X3 and Y0 == Y3:
                            f.write('({},{},{})'.format(X0,Y0,'bk'))    
                        else:
                            image = 0
                        if g < len(grid) - 1:
                            f.write(',') 
                        g += 1    
                    f.write('),')    
                    f.write('label={}\n'.format(game))    
                    
                    j += 1
                i += 1
            case += 1

createExamples(dataset = mnist_train_data, chess = chess, number_of_mate_cases = 300, number_of_draw_cases = 300, number_of_safe_cases = 300,
               examples_per_mate_case = 10, examples_per_draw_case = 10, examples_per_safe_case = 10,
               filename = data_root + "train_data.txt")

createExamples(dataset = mnist_test_data, chess = chess, number_of_mate_cases = 300, number_of_draw_cases = 300, number_of_safe_cases = 300,
               examples_per_mate_case = 10, examples_per_draw_case = 10, examples_per_safe_case = 10,
               filename = data_root + "test_data.txt")

