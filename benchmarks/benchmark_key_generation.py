from scarab import generate_pair
from benchmark import benchmark


benchmark(generate_pair, 100, verbose=True)