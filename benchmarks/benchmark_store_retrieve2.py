from scarab import generate_pair
from benchmarks.benchmark import benchmark
from common.utils import binary
from server import Store
import numpy as np

store = Store(database=np.array([[1, 1, 1, 1],
                                 [1, 1, 1, 0],
                                 [1, 1, 0, 0],
                                 [1, 0, 0, 0]]))
index = 2
pk, sk = generate_pair()
eq = pk.encrypt(binary(index, size=store.index_length), sk)


def func():
    list(store.retrieve2(eq, pk))

benchmark(func, 100, verbose=True)
