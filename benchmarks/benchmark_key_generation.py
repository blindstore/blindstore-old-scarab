import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")

from benchmarks.benchmark import benchmark
from scarab import generate_pair


benchmark(generate_pair, 100, verbose=True)