
import random
from utilities import computeFunction
from datasets import mnist_test_data, mnist_train_data, hasy_test_data, hasy_train_data
from params import data_root

def createExamples(symbols_dataset, digits_dataset, op_type, criterion, number_of_examples:int, number_of_symbols:int, filename:str):
    random.seed()

    with open(filename, 'a') as f:
        example_index = 0
        while example_index < number_of_examples:

            iteration = 0
            function_arguments = list()
            symbol_images_str = 'symbol_images=('
            while iteration < number_of_symbols:
                if iteration % 2 == 0:
                    image_index = random.randint(0,len(digits_dataset) - 1)
                    (_, digit) = digits_dataset[image_index]
                    function_arguments.append(digit)
                    symbol_images_str += str(image_index)
                else:
                    loop = True
                    while loop == True:
                        symbol_index = random.randint(0,len(symbols_dataset) - 1)
                        (_, op) = symbols_dataset[symbol_index]
                        if op == op_type:
                            loop = False
                            break
                    function_arguments.append(op)
                    symbol_images_str += str(symbol_index)
                if iteration < number_of_symbols - 1:
                    symbol_images_str += ','
                iteration += 1
            symbol_images_str += '),'
            digit3 = criterion(function_arguments)
            symbol_images_str += 'label={}\n'.format(digit3)
            f.write(symbol_images_str)
            example_index += 1

op_types = [4,5,6]

for op_type in op_types:
    createExamples(symbols_dataset = hasy_train_data, digits_dataset = mnist_train_data, op_type = op_type, criterion = computeFunction, number_of_examples = 1500, number_of_symbols = 18, filename = data_root + "symbols_math/18/train_data.txt")
    createExamples(symbols_dataset = hasy_test_data, digits_dataset = mnist_test_data, op_type = op_type, criterion = computeFunction, number_of_examples = 3000, number_of_symbols = 18, filename = data_root + "symbols_math/18/test_data.txt")
