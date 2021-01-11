
def computePositiveAndNegativeCases(number_of_symbols):
    
    if number_of_symbols == 5:
        formating = '{0:05b}'
    elif number_of_symbols == 7:
        formating = '{0:07b}'
    elif number_of_symbols == 10:
        formating = '{0:010b}'
    elif number_of_symbols == 15:
        formating = '{0:015b}'
    elif number_of_symbols == 18:
        formating = '{0:018b}'
    else:
        return ValueError 
    
    positive = list()
    negative = list()
    number = 0
    while number < (2**number_of_symbols) - 1:
        binary = formating.format(number)         
        i = 1
        while i < number_of_symbols - 1: 
            j = 1
            while j < number_of_symbols - 1:
                
                newbinary = [int(x) for x in list(formating.format(number))]
                
                newbinary[i] = '='
                newbinary[j] = '+'
                                
                if abs(i - j) > 1 and i < j:
                    result = binary[0:i]
                    number1 = binary[i+1:j]
                    number2 = binary[j+1:]
                    if int(result, 2) == int(number1, 2) + int(number2, 2) and newbinary not in positive:
                        positive.append(newbinary)
                    elif int(result, 2) != int(number1, 2) + int(number2, 2) and newbinary not in negative: 
                        negative.append(newbinary)
                            
                elif abs(i - j) > 1 and i > j:
                    number1 = binary[0:j]
                    number2 = binary[j+1:i]
                    result = binary[i+1:]
                    if int(result, 2) == int(number1, 2) + int(number2, 2) and newbinary not in positive:
                        positive.append(newbinary)
                    elif int(result, 2) != int(number1, 2) + int(number2, 2) and newbinary not in negative: 
                        negative.append(newbinary)
                elif newbinary not in negative: 
                    negative.append(newbinary)
            
                j = j + 1
                
            i = i + 1
        
        number = number + 1

    return (positive,negative)