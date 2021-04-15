nr_epochs = 3
minibatch_size = 1
learning_rate = 0.001
number_of_training_examples = 3001
data_root = '../../data/'
models_root = '../../models/'
proofs_root = '../../proofs/'
results_root = '../../results/'
logs_root = '../../logs/'
snapshot_iter = 100
shuffle = True
useGPU = False
# path to SICStus bin directory
sicstus_bin = '/home/marios/Downloads/sicstus_bin/'


def printparams():
    print("nr_epochs  = " + str(nr_epochs))
    print("minibatch_size = " + str(minibatch_size))
    print("learning_rate = " + str(learning_rate))
    print("number_of_training_examples = " + str(number_of_training_examples))
    print("data_root = " + str(data_root))
    print("models_root = " + str(models_root))
    print("snapshot_iter = " + str(snapshot_iter))
    print("shuffle = " + str(shuffle))
    print("useGPU = " + str(useGPU))
