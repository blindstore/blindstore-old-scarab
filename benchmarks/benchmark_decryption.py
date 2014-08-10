import sys.path
import os.path
# Import from sibling directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")

from scarab import generate_pair
from benchmark import benchmark_precise
from common.utils import binary


pk, sk = generate_pair()
index = binary(42, size=8)
encrypted_one = pk.encrypt(1)


def func():
    sk.decrypt(encrypted_one)


benchmark_precise(func, 10000, verbose=True)
