from scarab import generate_pair
from benchmarks.benchmark import Benchmark
from common.utils import binary


pk, sk = generate_pair()
index = binary(42, size=8)


def func():
    pk.encrypt(index, sk)


b = Benchmark(func)
b.run(100, verbose=True)
