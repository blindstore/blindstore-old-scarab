"""Test cryptographic utilities"""

from contracts.interface import ContractNotRespected
from gmpy2 import mpz, is_odd, random_state
from nose.tools import *

from blindstore.core.crypto.utils import *


def test_make_random_state():
    s1 = RandomState()
    assert_true(isinstance(s1, RandomState))
    s2 = RandomState(1000)
    assert_true(isinstance(s2, RandomState))


def test_random_odd_type_error():
    assert_raises(ContractNotRespected, random_odd_mpz, None, None)
    assert_raises(ContractNotRespected, random_odd_mpz, 1, 2)
    assert_raises(ContractNotRespected, random_odd_mpz, mpz(1), mpz(2), 'whatever')


def test_random_odd_semantic_error():
    assert_raises(ValueError, random_odd_mpz, mpz(2), mpz(0))


def test_random_odd_correct():
    ranges = [(2, 10), (3, 10), (3, 11), (2, 11), (-10, 10), (-11, 11)]
    for a, b in ranges:
        for _ in range(1000):
            x = random_odd_mpz(mpz(a), mpz(b))
            assert_true(is_odd(x))
            assert_true(mpz(a) <= x <= mpz(b))


def test_random_type_error():
    assert_raises(ContractNotRespected, random_mpz, None, None)
    assert_raises(ContractNotRespected, random_mpz, 1, 2)
    assert_raises(ContractNotRespected, random_mpz, mpz(1), mpz(2), 'whatever')


def test_random_semantic_error():
    assert_raises(ValueError, random_mpz, mpz(2), mpz(0))


def test_random_correct():
    ranges = [(2, 10), (3, 10), (3, 11), (2, 11), (-10, 10), (-11, 11)]
    for a, b in ranges:
        for _ in range(1000):
            x = random_mpz(mpz(a), mpz(b))
            assert_true(mpz(a) <= x <= mpz(b))