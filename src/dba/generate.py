
import random
from datasets import mnist_test_data, mnist_train_data
from params import data_root
from dba.utilities import computePositiveAndNegativeCases

def createDatasetDictionary(dataset):
    
    dataset_indices = list(range(len(dataset)))
    image_indices_dict = dict()
    
    for image_id in dataset_indices:
        (_, sign) = dataset[image_id]
        if sign not in image_indices_dict:
            image_indices_dict[sign] = list()
        image_indices_dict[sign].append(image_id)
        
    return image_indices_dict

def chooseImages(digits_dict, binary):
    index = 0
    symbols = ''
    while index < len(binary):
        
        symbol = binary[index]
        if symbol == 0: 
            data = digits_dict[0]
        elif symbol == 1: 
            data = digits_dict[1]
        elif symbol == '+': 
            data = digits_dict[4]
        elif symbol == '=': 
            data = digits_dict[3]

        random_index = random.randint(0,len(data) - 1)
        image = data[random_index]        
        
        symbols += str(image)
        
        if index < len(binary) - 1:
            symbols += ','
            
        index += 1
            
    return symbols
        
def createExamples(train_dataset, test_dataset, number_of_examples:int, number_of_symbols:int, trainfilename:str, testfilename:str):
    random.seed()
    digits_dict_train = createDatasetDictionary(train_dataset)
    digits_dict_test = createDatasetDictionary(test_dataset)
    
    (positive,negative) = computePositiveAndNegativeCases(number_of_symbols)
    
    with open(trainfilename, 'a') as ftrain:
        with open(testfilename, 'a') as ftest:
            example_index = 0
            while example_index < number_of_examples:
                
                if random.random() < 0.5:
                    number = random.randint(0,len(positive) - 1)
                    example = positive[number]
                    flag = True
                else:                
                    number = random.randint(0,len(negative) - 1)
                    example = negative[number]
                    flag = False
                    
                symbols = chooseImages(digits_dict_train, example)
                example_str = 'symbol_images=('
                example_str += symbols
                example_str += '),'
                example_str += 'label={}\n'.format(flag)
                ftrain.write(example_str)
                ftrain.write('#{}\n'.format(example))
                
                ###################################################
                
                symbols = chooseImages(digits_dict_test, example)
                example_str = 'symbol_images=('
                example_str += symbols
                example_str += '),'
                example_str += 'label={}\n'.format(flag)
                ftest.write(example_str)
                ftest.write('#{}\n'.format(example))
                
                symbols = chooseImages(digits_dict_test, example)
                example_str = 'symbol_images=('
                example_str += symbols
                example_str += '),'
                example_str += 'label={}\n'.format(flag)
                ftest.write(example_str)
                ftest.write('#{}\n'.format(example))
                
                symbols = chooseImages(digits_dict_test, example)
                example_str = 'symbol_images=('
                example_str += symbols
                example_str += '),'
                example_str += 'label={}\n'.format(flag)
                ftest.write(example_str)
                ftest.write('#{}\n'.format(example))
                
                example_index += 1


createExamples(train_dataset = mnist_train_data, test_dataset = mnist_test_data, number_of_examples = 3500, number_of_symbols = 7, trainfilename = data_root + "dba/7/train_data.txt", testfilename = data_root + "dba/7/test_data.txt")
#createExamples(digits_dataset = mnist_test_data, number_of_examples = 10000, number_of_symbols = 10, filename = data_root + "dba/10/test_data.txt")


