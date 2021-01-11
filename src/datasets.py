
import torchvision
import torchvision.transforms as transforms
from params import data_root

transform_mnist = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.5,), (0.5, ))])
mnist_train_data = torchvision.datasets.MNIST(root = data_root + 'MNIST', train=True, download=True,transform=transform_mnist)
mnist_test_data = torchvision.datasets.MNIST(root = data_root + 'MNIST', train=False, download=True,transform=transform_mnist)

mnist_train_images = torchvision.datasets.MNIST(root = data_root + 'MNIST', train=True, download=True)
mnist_test_images = torchvision.datasets.MNIST(root = data_root + 'MNIST', train=False, download=True)

transform_hasy = transforms.Compose([transforms.Grayscale(1), transforms.ToTensor(), transforms.Normalize((0.5,), (0.5, ))])
hasy_train_data = torchvision.datasets.ImageFolder(root = data_root + 'hasy/train', transform=transform_hasy)
hasy_test_data = torchvision.datasets.ImageFolder(root = data_root + 'hasy/test', transform=transform_hasy)
