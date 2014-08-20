"""Test HE"""

from contracts.interface import ContractNotRespected
from gmpy2 import mpz, is_odd, random_state, digits
from nose.tools import *

from blindstore.core.crypto.vdghv import *
from blindstore.core.crypto.utils import *


class TestPublicKey(object):

    def setup(self):
        self.data = mpz(7**42)

    def test_init_incorrect_type(self):
        data = 1
        assert_raises(ContractNotRespected, PublicKey, data)

    def test_init_incorrect_str(self):
        data = ':-('
        assert_raises(ValueError, PublicKey, data)

    def test_init_mpz(self):
        pk = PublicKey(self.data)
        assert_true(isinstance(pk, PublicKey))

    def test_init_str(self):
        data = digits(self.data, PublicKey.radix)
        pk = PublicKey(data)
        assert_true(isinstance(pk, PublicKey))

    def test_serialization(self):
        pk1 = PublicKey(self.data)
        pk2 = PublicKey(str(pk1))
        assert_equals(pk1.data, pk2.data)


class TestPrivateKey(object):

    def setup(self):
        self.data = mpz(7**42)

    def test_init_incorrect_type(self):
        data = 1
        assert_raises(ContractNotRespected, PrivateKey, data)

    def test_init_incorrect_str(self):
        data = ':-('
        assert_raises(ValueError, PrivateKey, data)

    def test_init_mpz(self):
        pk = PrivateKey(self.data)
        assert_true(isinstance(pk, PrivateKey))

    def test_init_str(self):
        data = digits(self.data, PrivateKey.radix)
        pk = PrivateKey(data)
        assert_true(isinstance(pk, PrivateKey))

    def test_serialization(self):
        pk1 = PrivateKey(self.data)
        pk2 = PrivateKey(str(pk1))
        assert_equals(pk1.data, pk2.data)



class TestCiphertext(object):

    def setup(self):
        self.pk = PublicKey(mpz(42))
        self.data = [mpz(42), mpz(42), mpz(42)]

    def test_init_incorrect_type(self):
        assert_raises(ContractNotRespected, Ciphertext, 1, 1)
        assert_raises(ContractNotRespected, Ciphertext, self.pk, 1)
        assert_raises(ContractNotRespected, Ciphertext, 1, self.data)

    def test_init(self):
        c = Ciphertext(self.pk, self.data)
        assert_true(isinstance(c, Ciphertext))

    def test_serialization(self):
        c1 = Ciphertext(self.pk, self.data)
        c2 = Ciphertext(self.pk, str(c1))
        assert_equals(c1.data, c2.data)

    def test_len(self):
        c = Ciphertext(self.pk, self.data)
        assert_equals(len(c), len(self.data))


class TestContext(object):

    def test_generate_keypair(self):
        context = Context(30, 60)
        assert_true(isinstance(context.pk, PublicKey))

    def test_encryption(self):
        context = Context(5)
        cases = [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1],
            [0, 0, 0, 1, 0],
            [0, 0, 1, 0, 0],
            [0, 1, 0, 0, 0],
            [1, 0, 0, 0, 0],
            [1, 1, 1, 1, 1],
            [1, 0, 1, 0, 1],
            [1, 1, 1, 0, 0],
            [0, 0, 1, 1, 1],
        ]
        for case in cases:
            c = context.encrypt(case)
            m = context.decrypt(c)
            assert_equals(m, case)