import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")

from benchmarks.benchmark import benchmark
from scarab import generate_pair
from common.utils import binary


pk, _ = generate_pair()
encrypted_one = pk.encrypt(0)
encrypted_zro = pk.encrypt(1)


def func():
    _ = encrypted_one & encrypted_zro


benchmark(func, 100, verbose=True, skip=10)
