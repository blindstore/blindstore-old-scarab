import os
import sys
from functools import reduce
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")

from benchmarks.benchmark import benchmark
from scarab import generate_pair
from common.utils import binary

_AND = lambda a, b: a & b

# This is a naive approach of calculating gammas
pk, _ = generate_pair()
index_to_find = binary(32, size=32)
index_to_find_enc_bit_array = pk.encrypt(index_to_find)

index_in_store = binary(32, size=32) # can be a whatever number. it is just for testing

def gamma_naive(a_hats, index_bit_array):
    pre_gamma = []
    for i, a_hat in enumerate(a_hats):
        pre_gamma.append( pk.encrypt(index_bit_array[i]) ^ pk.encrypt(1) ^ a_hat )

    return reduce(_AND, pre_gamma)

def func():
  gamma_naive(index_to_find_enc_bit_array, index_in_store)

benchmark(func, 10, verbose=True)
