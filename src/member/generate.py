
import random
from datasets import mnist_test_data, mnist_train_data
from params import data_root

def createExamples(dataset, number_of_examples:int, number_of_arguments:int, filename:str):
    random.seed()    
    image_indices = list()
    example_index = 0
    while example_index <= number_of_examples:
        image_indices_per_example = list()
        argument_index = 0
        while argument_index < number_of_arguments:
            image_index = random.randint(0,len(dataset) - 1) 
            image_indices_per_example.append(image_index)
            argument_index = argument_index + 1
        image_indices.append(image_indices_per_example) 
        example_index = example_index + 1
    
    with open(filename, 'w') as f:
        for image_indices_per_example in image_indices:
            if random.random() < 0.75:          
                f.write('digit_images=(')
                index = 0
                while index < len(image_indices_per_example):
                    f.write('{}'.format(image_indices_per_example[index]))
                    if index < len(image_indices_per_example) - 1:
                        f.write(',')
                    index += 1
                f.write('),')
                
                image_index = random.randint(0, len(image_indices_per_example) - 1) 
                (_, digit) = dataset[image_indices_per_example[image_index]]      
                f.write('target={},label={}\n'.format(digit,True))
            else:
                f.write('digit_images=(')
                index = 0
                while index < len(image_indices_per_example):
                    f.write('{}'.format(image_indices_per_example[index]))
                    if index < len(image_indices_per_example) - 1:
                        f.write(',')
                    index += 1
                f.write('),')
                digits_current_iteration = list()
                for image_id in image_indices_per_example:
                    (_, digit) = dataset[image_id]
                    digits_current_iteration.append(digit)
                
                not_member_digit = random.randint(0, 9)
                while not_member_digit in digits_current_iteration:
                    not_member_digit = random.randint(0, 9)
                f.write('target={},label={}\n'.format(not_member_digit,False))

createExamples(dataset = mnist_train_data, number_of_examples = 100000, number_of_arguments = 5, filename = data_root + "memberOf/5/train_data.txt")
createExamples(dataset = mnist_test_data, number_of_examples = 100000, number_of_arguments = 5, filename = data_root + "memberOf/5/test_data.txt")
