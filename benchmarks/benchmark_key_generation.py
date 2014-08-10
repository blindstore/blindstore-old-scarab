from scarab import generate_pair
from benchmarks.benchmark import benchmark


benchmark(generate_pair, 100, verbose=True)