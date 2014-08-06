from scarab import generate_pair
from benchmarks.benchmark import Benchmark
from common.utils import binary


pk, sk = generate_pair()
index = binary(42, size=8)
encrypted_one = pk.encrypt(1)
encrypted_zro = pk.encrypt(0)


def func():
    _ = encrypted_one & encrypted_zro


b = Benchmark(func)
b.run(100, verbose=True, skip=10)
