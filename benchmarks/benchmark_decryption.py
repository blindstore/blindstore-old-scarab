from scarab import generate_pair
from benchmarks.benchmark import benchmark_precise
from common.utils import binary


pk, sk = generate_pair()
index = binary(42, size=8)
encrypted_one = pk.encrypt(1)


def func():
    sk.decrypt(encrypted_one)


benchmark_precise(func, 10000, verbose=True)
