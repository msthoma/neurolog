import torch
from networks.mnist_nets import COMP_NET
from member.abduction import Abduction
from member.manager import MemberManager
from abstract_translator import AbstractTranslator
from params import useGPU, sicstus_bin
from run import scenario_train
from member.abducibles import abducibles, exclusive    
from member.local_params import number_of_arguments
    
network = COMP_NET()
if useGPU:
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    network.to(device)
    
translator = AbstractTranslator(abducibles, exclusive)
dataManager = MemberManager()
abduction = Abduction(sicstus_bin, translator)
outputClasses = [10] * number_of_arguments
scenario = 'member/' + str(number_of_arguments)

scenario_train(network, outputClasses, translator, dataManager, scenario, abduction)


