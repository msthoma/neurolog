import torch
from networks.mnist_nets import COMP_NET
from abstract_translator import AbstractTranslator
from member.manager import MemberManager
from member.evaluate import Evaluator
from params import useGPU
from run import scenario_test
from member.abducibles import abducibles, exclusive    
from member.local_params import number_of_arguments

network = COMP_NET()
if useGPU:
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    network.to(device)
    
translator = AbstractTranslator(abducibles, exclusive)
dataManager = MemberManager()
outputClasses = [10] * number_of_arguments
evaluator = Evaluator()
scenario = 'member/' + str(number_of_arguments)
model_name = 'model_samples_3000_iter_400_epoch_1.mdl'

scenario_test(network, outputClasses, translator, dataManager, scenario, model_name, evaluator)
