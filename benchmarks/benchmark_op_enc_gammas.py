import os
import sys
from functools import reduce
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")

from benchmarks.benchmark import benchmark
from scarab import generate_pair
from common.utils import binary

_AND = lambda a, b: a & b

# Get a store that has cached:
#   a) a bin array of the indices
#   b) encrypted(1) HM_XOR encrypted(1)
#   c) encrypted(0) HM_XOR encrypted(1)
# We need to print and play with the lengths of:
#   a) encrypted(1)
#   b) encrypted(0)
#   c) encrypted(1) HM_XOR encrypted(1) (same for 0)
#   d) length of indices
#   e) num of indices
pk, _ = generate_pair()
index_to_find = binary(32, size=32)
index_to_find_enc_bit_array = pk.encrypt(index_to_find)

index_in_store = binary(32, size=32) # can be a whatever number. it is just for testing

enc_one = pk.encrypt(0)
enc_zero = pk.encrypt(1)

cached_enc_one_one = enc_zero ^ enc_one
cached_enc_zero_one = enc_one ^ enc_one
cached_reverse_encryptions = [cached_enc_one_one, cached_enc_zero_one]

def gamma(a_hats, index_bit_array):
    pre_gamma = []
    for i, a_hat in enumerate(a_hats):
        pre_gamma.append( cached_reverse_encryptions[index_bit_array[i]] ^ a_hat )

    return reduce(_AND, pre_gamma)

def func():
  gamma(index_to_find_enc_bit_array, index_in_store)

benchmark(func, 10, verbose=True)
