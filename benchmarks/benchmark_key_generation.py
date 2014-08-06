from scarab import generate_pair
from benchmarks.benchmark import Benchmark

b = Benchmark(generate_pair)

b.run(25, verbose=True)