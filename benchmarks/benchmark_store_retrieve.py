import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")

from benchmarks.benchmark import benchmark
from scarab import generate_pair
from common.utils import binary
from server import Store


store = Store(record_size=20, record_count=20, fill='random')
index = 2
pk, sk = generate_pair()
eq = pk.encrypt(binary(index, size=store.index_bits), sk)


def func():
    list(store.retrieve(eq, pk))

benchmark(func, 10, verbose=True)
