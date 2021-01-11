
from pysdd.sdd import SddManager, SddNode
import torch
from params import useGPU

def computeTensorWMC(node:SddNode, manager:SddManager, literal2OutputNeuron:dict, weights:torch.tensor)->torch.tensor:
    
    stack = list()
    nodesToTensors = dict()
    
    stack.append(node)
    
    while len(stack) > 0:
        
        top = stack[len(stack)-1]
        if top not in nodesToTensors:
            
            if top.is_decision():                

                noTensor = False
                for element in top.elements():
                    if element[0] not in nodesToTensors:
                        stack.append(element[0])
                        noTensor = True
                    if element[1] not in nodesToTensors:
                        stack.append(element[1])
                        noTensor = True
                
                if noTensor == False:
                    if useGPU:
                        result = torch.tensor([0.0], requires_grad = True).cuda()
                    else:
                        result = torch.tensor([0.0], requires_grad = True)
                    for element in top.elements():
                        result = result + nodesToTensors[element[0]] * nodesToTensors[element[1]]
                        
                    nodesToTensors[top] = result
                    stack.pop()
                
            elif top.is_literal():
                literal = top.literal
                if literal < 0:
                    positive = manager.literal(-literal)
                    neuronIndex = literal2OutputNeuron[positive]
                    nodesToTensors[top] = 1 - weights[neuronIndex]
                else:
                    neuronIndex = literal2OutputNeuron[top]
                    nodesToTensors[top] = weights[neuronIndex]    
                stack.pop()
                
            elif top.is_false():
                if useGPU:
                    nodesToTensors[top] = torch.tensor([0.0], requires_grad = True).cuda()
                else:
                    nodesToTensors[top] = torch.tensor([0.0], requires_grad = True)
                stack.pop()
                            
            elif top.is_true():
                if useGPU:
                    nodesToTensors[top] = torch.tensor([1.0], requires_grad = True).cuda()
                else:
                    nodesToTensors[top] = torch.tensor([1.0], requires_grad = True)
                stack.pop()
        else: 
            stack.pop()
    
    return nodesToTensors[node]
            
        
        