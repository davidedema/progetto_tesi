from typing import Mapping, Iterator    # import interfaccia Mapping e iterator)
                                        # Mapping agisce come dizionario, iterator serve per iterare    

import torch
import torchvision
import torchvision.transforms as transforms
from problog.logic import Term, Constant

from deepproblog.dataset import Dataset
from deepproblog.query import Query

# trasformazione che deve essere applicata alle immagini prima di addestrare la rete neurale.
# transform.ToTensor() converte le immagini in tensori (torch), immagini in scala di grigi in un tensore a una dimensione
# transform.Normalize() normalizza il tensore precedentemente creato, tensore risulta in un tensore con media 0 e varianza 1

transform = transforms.Compose(
    [transforms.ToTensor(), transforms.Normalize((0.5,), (0.5,))]
)

# definisce due dataset: train e test
# chiave sono le stringhe "train" e "test", valori sono i dataset

datasets = {
    "train": torchvision.datasets.MNIST(
        root='data/', train=True, download=True, transform=transform
    ),
    "test": torchvision.datasets.MNIST(
        root='data/', train=False, download=True, transform=transform
    ),
}


class MNISTImages(Mapping[Term, torch.Tensor]):

    def __iter__(self) -> Iterator:
        for i in range(self.dataset):
            yield self.dataset[i][0]

    def __len__(self) -> int:
        return len(self.dataset)

    def __init__(self, subset):
        self.subset = subset
        self.dataset = datasets[self.subset]

    def __getitem__(self, item):
        return self.dataset[int(item[0])][0]


class AdditionDataset(Dataset):

    def __init__(self, subset):
        self.subset = subset
        self.dataset = datasets[subset]

    def __len__(self):
        return len(self.dataset) // 2

    def to_query(self, i: int) -> Query:
        image1 = Term("tensor", Term(self.subset, Constant(i * 2)))
        image2 = Term("tensor", Term(self.subset, Constant(i * 2 + 1)))
        label = Constant(int(self.dataset[i*2][1] + self.dataset[i*2+1][1]))
        term = Term('addition', image1, image2, label)
        return Query(term)
