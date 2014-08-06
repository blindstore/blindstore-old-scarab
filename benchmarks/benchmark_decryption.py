from scarab import generate_pair
from benchmarks.benchmark import Benchmark
from common.utils import binary


pk, sk = generate_pair()
index = binary(42, size=8)
encrypted_one = pk.encrypt(1)


def func():
    sk.decrypt(encrypted_one)


b = Benchmark(func)
b.run_precise(10000, verbose=True)
