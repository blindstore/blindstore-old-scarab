from scarab import generate_pair
from benchmarks.benchmark import benchmark
from common.utils import binary
from server import Store


store = Store(record_size=20, record_count=20, fill='random')
index = 2
pk, sk = generate_pair()
eq = pk.encrypt(binary(index, size=store.index_length), sk)


def func():
    list(store.retrieve2(eq, pk))

benchmark(func, 10, verbose=True)
