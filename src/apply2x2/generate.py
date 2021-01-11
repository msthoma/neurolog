
from datasets import hasy_test_data, hasy_train_data
import random
from params import data_root
from utilities import computeFunction

def createExamples(dataset, op_types, number_of_examples, filename):
    random.seed()
    with open(filename,'w') as f:
        example_index = 0
        while example_index < number_of_examples:
            loop = True
            while loop == True:
                op1_index = random.randint(0,len(dataset) - 1)
                (_, op1) = dataset[op1_index]
                if op1 in op_types:
                    loop = False
                    break

            loop = True
            while loop == True:
                op2_index = random.randint(0,len(dataset) - 1)
                (_, op2) = dataset[op2_index]
                if op2 in op_types:
                    loop = False
                    break

            loop = True
            while loop == True:
                op3_index = random.randint(0,len(dataset) - 1)
                (_, op3) = dataset[op3_index]
                if op3 in op_types and op3 != 6:
                    loop = False
                    break

            loop = True
            while loop == True:
                op4_index = random.randint(0,len(dataset) - 1)
                (_, op4) = dataset[op4_index]
                if op4 in op_types and op4 != 6:
                    loop = False
                    break

            digit1 = random.randint(0,10)
            digit2 = random.randint(0,10)
            digit3 = random.randint(0,10)

            row1_result = computeFunction([digit1, op1, digit2, op2, digit3])
            row2_result = computeFunction([digit1, op3, digit2, op4, digit3])
            col1_result = computeFunction([digit1, op1, digit2, op3, digit3])
            col2_result = computeFunction([digit1, op2, digit2, op4, digit3])

            f.write('digit1={},digit2={},digit3={},op11_image={},op12_image={},op21_image={},op22_image={},row1_result={},row2_result={},col1_result={},col2_result={}\n'.\
                    format(digit1, digit2, digit3, op1_index, op2_index, op3_index, op4_index, row1_result, row2_result, col1_result, col2_result))
            example_index += 1

op_types = [4,5,6]

createExamples(hasy_train_data, op_types, 50000, data_root + "apply2x2/train_data.txt")
createExamples(hasy_test_data, op_types, 100000, data_root + "apply2x2/test_data.txt")
