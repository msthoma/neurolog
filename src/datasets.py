import torchvision
import torchvision.transforms as transforms

from src.params import data_root

# below I'm redefining the links to the MNIST dataset, since the original produces a 503 service unavailable error
torchvision.datasets.MNIST.resources = [
    ('https://ossci-datasets.s3.amazonaws.com/mnist/train-images-idx3-ubyte.gz', 'f68b3c2dcbeaaa9fbdd348bbdeb94873'),
    ('https://ossci-datasets.s3.amazonaws.com/mnist/train-labels-idx1-ubyte.gz', 'd53e105ee54ea40749a09fcbcd1e9432'),
    ('https://ossci-datasets.s3.amazonaws.com/mnist/t10k-images-idx3-ubyte.gz', '9fb629c4189551a2d022fa330f9573f3'),
    ('https://ossci-datasets.s3.amazonaws.com/mnist/t10k-labels-idx1-ubyte.gz', 'ec29112dd5afa0611ce80d1b7f02629c')
]

transform_mnist = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.5,), (0.5,))])
mnist_train_data = torchvision.datasets.MNIST(root=data_root + 'MNIST', train=True, download=True,
                                              transform=transform_mnist)
mnist_test_data = torchvision.datasets.MNIST(root=data_root + 'MNIST', train=False, download=True,
                                             transform=transform_mnist)

mnist_train_images = torchvision.datasets.MNIST(root=data_root + 'MNIST', train=True, download=True)
mnist_test_images = torchvision.datasets.MNIST(root=data_root + 'MNIST', train=False, download=True)

transform_hasy = transforms.Compose(
    [transforms.Grayscale(1), transforms.ToTensor(), transforms.Normalize((0.5,), (0.5,))])
hasy_train_data = torchvision.datasets.ImageFolder(root=data_root + 'hasy/train', transform=transform_hasy)
hasy_test_data = torchvision.datasets.ImageFolder(root=data_root + 'hasy/test', transform=transform_hasy)
