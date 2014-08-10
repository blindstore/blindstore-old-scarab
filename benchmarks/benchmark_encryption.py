from scarab import generate_pair
from benchmarks.benchmark import benchmark

from common.utils import binary


pk, sk = generate_pair()
index = binary(42, size=8)


def func():
    pk.encrypt(index, sk)


benchmark(func, 100, verbose=True)
