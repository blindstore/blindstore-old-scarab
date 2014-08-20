# -*- coding: utf-8 -*-

"""V-DGHV somewhat homomorphic encryption scheme implementation

Scheme was proposed in Single Database Private Information Retrieval from
Fully homomorphic Encryption by Yi et al. (doi:10.1109/TKDE.2012.90)

.. note::

   Uses PyContracts for type validation, since gmpy segfaults happily
   when types are incorrect.

.. moduleauthor:: Bogdan Kulynych <bogdan.kulynych@gmail.com>

"""

import json

from contracts import contract, new_contract
from gmpy2 import mpz, \
    random_state, mpz_random, \
    is_odd, digits, f_mod

from .utils import one, two, random_odd_mpz, random_mpz, mpz_t


# Type contracts
new_contract('PublicKey', lambda s: isinstance(s, PublicKey))
new_contract('PrivateKey', lambda s: isinstance(s, PrivateKey))
new_contract('Ciphertext', lambda s: isinstance(s, Ciphertext))


class PublicKey(object):

    """Public key"""

    radix = 62

    @contract
    def __init__(self, pk):
        """Create Public key object

        :param pk: public key raw represenation
        :type pk: str|mpz
        """
        if isinstance(pk, str):
            self.data = mpz(pk, PublicKey.radix)
        elif isinstance(pk, mpz_t):
            self.data = mpz(pk)

    def __str__(self):
        """Serialize public key"""
        return digits(self.data, PublicKey.radix)


class PrivateKey(object):

    """Private key"""

    radix = 62

    @contract
    def __init__(self, sk):
        """Create Private key object

        :param sk: private key raw represenation
        :type sk: str|mpz
        """
        if isinstance(sk, str):
            self.data = mpz(sk, PrivateKey.radix)
        elif isinstance(sk, mpz_t):
            self.data = mpz(sk)

    def __str__(self):
        """Serialize private key"""
        return digits(self.data, PrivateKey.radix)


class Ciphertext(object):

    """Ciphertext"""

    radix = 62

    @contract
    def __init__(self, pk, cipher_bits):
        """Create Ciphertext object

        :param pk: :class:`PublicKey` object
        :type pk: PublicKey
        :param cipher_bits: list of cipher bits
        :type cipher_bits: str|list(mpz)
        """
        self.pk = pk
        if isinstance(cipher_bits, str):
            cipher_bits = json.loads(cipher_bits)
            self.data = [mpz(c, Ciphertext.radix) for c in cipher_bits]
        elif isinstance(cipher_bits, list):
            self.data = cipher_bits

    @contract
    def __add__(self, other):
        """Homomorphic addition (XOR)

        :type other: Ciphertext
        """
        pass

    __xor__ = __add__

    @contract
    def __mul__(self, other):
        """Homomorphic multiplication (AND)

        :type other: Ciphertext
        """
        pass

    __and__ = __mul__

    def __len__(self):
        """Number of encrypted bits"""
        return len(self.data)

    def __str__(self):
        """Serialize ciphertext to JSON string"""
        array = [digits(c, Ciphertext.radix) for c in self.data]
        return json.dumps(array)


class Context(object):

    """Public and private key pair"""

    @contract
    def __init__(self, l, s=60):
        """Generate HE key pair.

        Corresponds to HE.KEYGEN(s) procedure

        :param l: ciphertext size
        :type l: int, >0
        :param s: security parameter
        :type s: int, >0
        """
        λ = mpz(s)
        η = mpz((s + 3) * l)
        γ = mpz(5*(s + 3) * l // 2)

        self.λ = λ
        self.γ = γ

        a = two**(η - 1) + 1
        b = two**(η) - 1
        p = random_odd_mpz(a, b)

        assert (len(digits(p, 2)) == η)

        self.w = two**γ // p - 1

        q = random_odd_mpz(one, self.w)

        self.pk = PublicKey(q * p)
        self.sk = PrivateKey(p)

    @contract
    def encrypt(self, bits, reuse_parameters=False):
        """Encrypt list of bits. Both private key and private key needed

        Corresponds to HE.ENCRYPT(pk, m) procedure

        :param bits: list of bits
        :type bits: list[int]
        :param reuse_parameters: if True, will generate q, r only once.
            If False, will generate new q, r for every bit
        :type reuse_parameters: bool
        :rtype: Ciphertext
        """
        p = self.sk.data
        x = self.pk.data

        def generate_parameters():
            t = 2**self.λ
            return random_mpz(one, self.w), random_mpz(-t + 1, t - 1)

        q, r = generate_parameters()

        cipher_bits = []
        for m in bits:

            cipher = f_mod(m + 2*r + q*p, x)
            cipher_bits.append(cipher)

            if not reuse_parameters:
                q, r = generate_parameters()

        return Ciphertext(self.pk, cipher_bits)

    @contract
    def decrypt(self, ciphertext):
        """Decrypt ciphertext. Only requires private key

        Corresponds to HE.DECRYPT(sk, c) procedure

        :type ciphertext: Ciphertext
        :rtype: list[int]
        """
        p = self.sk.data

        bits = []
        for c in ciphertext.data:
            m = int(f_mod(f_mod(c, p), 2))
            bits.append(m)

        return bits