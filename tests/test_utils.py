import numpy as np
import scarab
from nose.tools import *

from common.utils import *


def test_binary():
    a = binary(1, size=5)
    assert_true(np.all(a == [0, 0, 0, 0, 1]))
    a = binary(2, size=3)
    assert_true(np.all(a == [0, 1, 0]))

def test_encrypt_index():
    pk, sk = scarab.generate_pair()
    c = encrypt_index(pk, 1, 5)
    assert_true(len(c) == 5)