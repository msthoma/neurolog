
from typing import List
import torch
import torch.nn as nn
from torch.optim import Optimizer

from loss import computeTensorWMC
from logger import Logger
from params import useGPU

import time
import random

class Trainer(object):

    def __init__(self, network:nn.Module, outputClasses:List, benchmarkManager, optimizer:Optimizer, translator, abduction, model_path:str):
        self.network = network
        self.benchmarkManager = benchmarkManager
        self.optimizer = optimizer
        self.translator = translator
        self.model_path = model_path
        self.abduction = abduction
        self.outputClasses = outputClasses
        
        self.manager = self.translator.getSddmanager() 
        self.literal2OutputNeuron = self.translator.getSddLiteralsToOutputNeurons()        
            
    def saveState(self, filename):
        torch.save(self.network.state_dict(), self.model_path + filename)
        
    def computeNeuralObservations(self, nnoutput)->bool:
        facts = list()
        start = 0
        for index in range(len(self.outputClasses)):
            _, predicted = torch.max(nnoutput.data[0,start:start + self.outputClasses[index]], 0)
            facts.append(self.translator.toFact(predicted.item() + start))
            start = start + self.outputClasses[index]
        
        observations = list()
        for fact in facts:
            if fact[3] != 'e':
                observations.append(fact)

        return observations
    
    def train(self, examples:List, nr_epochs, minibatch_size = 50, log_iter = 100, snapshot_iter = None, snapshot_name = 'model', shuffle = True, neural_guided_abduction = False, logs_path = '/'):

        iterations = 1
        total_loss = 0
         
        batch = list()
        logger = Logger()
        start = time.time()
        print("Training for {} epochs ({} iterations).".format(nr_epochs, nr_epochs * len(examples)))

        f = open(logs_path + "log.txt", "a") 
        for epoch in range(nr_epochs):
            epoch_start = time.time()
            print("Epoch", epoch + 1)
            indices = list(range(len(examples)))

            if shuffle:
                random.shuffle(indices)

            for index in indices:
                iteration_time = time.time()
                
                example = examples[index]
                
                batch.append(example)
                                
                if iterations % minibatch_size == 0:
  
                    observations = list()
                    nnoutputs = list()
                    for batch_element in batch:
                        nninput = self.benchmarkManager.computeNeuralInput(batch_element, dataset = 'train')
                        nnoutput = self.network(nninput)
                        observations.append(self.computeNeuralObservations(nnoutput))
                        nnoutputs.append(nnoutput)
                        
                    weights = torch.cat(nnoutputs, 0)
                    
                    loss = torch.tensor([0.0], requires_grad = True)
                    if (useGPU):
                        loss = torch.tensor([0.0], requires_grad = True).cuda()
                    
                    for index2 in range(len(batch)):
                        
                        batch_element = batch[index2]
                                                
                        goal = self.benchmarkManager.computeGoal(batch_element)

                        #Perform abduction
                        if neural_guided_abduction == False:
                            sddnode = self.abduction.abduce(goal)    
                        else: 
                            sddnode = self.abduction.abduce(goal, observations[index2])        

                        wmc = computeTensorWMC(sddnode, self.manager, self.literal2OutputNeuron, weights[index2,:])                        
                        if wmc > 9.2885e-30:
                            loss = loss - torch.log(wmc)
                        
                    if loss != 0:    
                        self.optimizer.zero_grad()
                        loss.backward()
                        self.optimizer.step()
                        total_loss += float(loss)
                                   
                    del weights, nninput, wmc
                    del batch[:], batch 
                    batch = list()
                    del nnoutputs[:], nnoutputs
                    
                if snapshot_iter and iterations % snapshot_iter == 0:
                    fname = '{}_samples_{}_iter_{}_epoch_{}.mdl'.format(snapshot_name, len(examples), iterations, epoch + 1)
                    self.saveState(fname)
                    
                if iterations % log_iter == 0:
                    f.write('{}\t{}\n'.format(iterations, time.time() - start))
                    print('Iteration: ', iterations, '\tAverage Loss: ', total_loss/log_iter, '\tTime', time.time() - start)
                    logger.log('time', iterations, iteration_time - start)
                    logger.log('loss', iterations, total_loss/log_iter)
                    total_loss = 0
                
                iterations += 1
                
            print('Epoch time: ', time.time() - epoch_start) 
            fname = '{}_samples_{}_iter_{}_epoch_{}.mdl'.format(snapshot_name, len(examples), iterations, epoch + 1)
            self.saveState(fname)
                
        ellapsedTime = (time.time() - start)
        ellapsedTimeMinutes = int(ellapsedTime/60)
        ellapsedTimeSeconds =int(ellapsedTime - ellapsedTimeMinutes*60)  
        print('Total training time: {}m{}s.'.format(ellapsedTimeMinutes, ellapsedTimeSeconds))
        f.close()
        return logger
    
    
