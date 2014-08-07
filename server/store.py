from functools import reduce

import numpy as np

import random
import numpy as np
from common.utils import binary, index_bits


_AND = lambda a, b: a & b
_XOR = lambda a, b: a ^ b


def _gamma(cipher_query, cipher_index, cipher_one):
    """
    Calculates the value of the gamma function, as described in PDF
    (paragraph 3.1.2)
    :param cipher_query: cipher query
    :param cipher_index: cipher index
    :param cipher_one: cipher one
    :return: the value of the gamma function
    """
    return reduce(_AND, [x for x in cipher_query ^ cipher_index], cipher_one)


def _R(gammas, column, cipher_zero):
    """
    Calculates the value of R() function, as described in PDF (paragraph 3.1.3)
    :param gammas: gammas
    :param column: column
    :param enc_zero: encrypted zero
    :return: the value of the R function
    """
    return reduce(_XOR, gammas[np.where(column == 1)], cipher_zero)


class Store:
    """A private store."""

    def __init__(self, record_size=3, record_count=5, database=None, fill=0):
        """
        Creates a new private store.
        :param record_size: the size of each record, in bits.
        :param record_count: the number of records.
        :param database: numpy matrix of database values.
        :param fill: value to fill the database with.
        """
        if database is None:
            array = None
            if fill == 'random':
                array = [[random.randint(0, 1) for _ in range(record_size)]
                    for _ in range(record_count)]
            else:
                array = [[fill] * record_size for _ in range(record_count)]
            database = np.array(array)

        self.record_count, self.record_size = database.shape
        self.database = database
        self.index_bits = index_bits(self.record_count)

        # precompute binary representation for index
        self.binary_index = [binary(x, size=self.index_bits) \
            for x in range(self.record_count)]

    def retrieve(self, cipher_query, public_key):
        """
        Retrieves an encrypted record from the store, given a ciphered query.
        :param cipher_query: the encrypted index of the record to retrieve, as
                             an :class:`~EncryptedArray`
        :param public_key: the :class:`~PublicKey` to use.
        :raises ValueError: if the length of cipher_query does not equal the \
                            Store's index_blength.
        """
        cipher_one = public_key.encrypt(1)
        cipher_zero = public_key.encrypt(0)

        def gamma(bits):
            bits = public_key.encrypt(bits)
            bits = _gamma(cipher_query, bits, cipher_one)
            return bits

        # TODO: make this parallel
        gammas = np.array([gamma(bits) for bits in self.binary_index])

        assert (len(gammas) == self.record_count)

        # TODO: make this parallel
        return [_R(gammas, self.database[:, x], cipher_zero) \
            for x in range(self.record_size)]

    def set(self, i, value):
        """
        Set a value in the array.
        :param i: the unencrypted index to set.
        :param value: the unencrypted value.
        """
        if len(value) < self.record_size:
            padded_value = np.zeros(self.record_size, dtype=np.int)
            padded_value[padded_value.size - len(value):] = value
        else:
            padded_value = value

        self.database[i] = padded_value