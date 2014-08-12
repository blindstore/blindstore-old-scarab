import sys
import os.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")

from benchmarks.benchmark import benchmark
from scarab import generate_pair
from common.utils import binary


pk, sk = generate_pair()
index = binary(42, size=8)


def func():
    pk.encrypt(index, sk)


benchmark(func, 100, verbose=True)
