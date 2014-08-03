from functools import reduce
import numpy as np
import time
import math

from scarab import generate_pair

from common.utils import binary, index_length


_ADD = lambda a, b: a + b
_MUL = lambda a, b: a * b
_AND = lambda a, b: a & b
_XOR = lambda a, b: a ^ b


def _gamma(cq, ci, co):
    """
    Calculates the value of the gamma function, as described in PDF (paragraph 3.1.2)
    :param cq: cipher query
    :param ci: cipher index
    :param co: cipher one
    :return: the value of the gamma function
    """
    return reduce(_AND, [x ^ co for x in cq ^ ci])


def _R(gammas, column, public_key):
    """
    Calculates the value of R() function, as described in PDF (paragraph 3.1.3)
    :param gammas: gammas
    :param column: column
    :param public_key: public key
    :return: the value of the R function
    """
    return reduce(_XOR, gammas[np.where(column == 1)], public_key.encrypt(0))


class Store:
    """A private store."""

    def __init__(self, record_size=3, record_count=5):
        """
        Creates a new private store.
        :param record_size: the size of each record, in bits.
        :param record_count: the number of records that can be stored.
        """
        self.record_size = record_size
        self.record_count = record_count
        self.index_length = index_length(record_count)
        self.database = np.array(
            [[1] * min(self.record_size, x) + [0] * max(0, self.record_size - x) for x in range(self.record_count)])

    def retrieve(self, cipher_query, public_key):
        """
        Retrieves an encrypted record from the store, given a ciphered query.
        :param cipher_query: the encrypted index of the record to retrieve, as
                             an :class:`~EncryptedArray`
        :param public_key: the :class:`~PublicKey` to use.
        """
        if len(cipher_query) != self.index_length:
            msg = "The cipher query length ({0} bits) is incorrect. It should be {1} bits long."
            raise ValueError(msg.format(len(cipher_query), self.index_length))

        indices = [binary(x, size=self.index_length) for x in range(self.record_count)]
        cipher_indices = [public_key.encrypt(index) for index in indices]
        cipher_one = public_key.encrypt(1)
        gammas = np.array([_gamma(cipher_query, ci, cipher_one) for ci in cipher_indices])

        tmp = []
        for c in range(self.record_size):
            column = self.database[:, c]
            tmp.append(_R(gammas, column, public_key))

        return tmp

    def set(self, index, value):
        """
        Set a value in the array.
        :param index: the unencrypted index to set.
        :param value: the unencrypted value.
        """
        if len(value) < self.record_size:
            paddedValue = np.zeros(self.record_size, dtype=np.int)
            paddedValue[paddedValue.size - len(value):] = value
        else:
            paddedValue = value

        self.database[index] = paddedValue


if __name__ == '__main__':
    store = Store()
    pk, sk = generate_pair()
    index = 2
    a = time.clock()
    enc_data = store.retrieve(pk.encrypt(binary(index, size=store.index_length)), pk)
    print([sk.decrypt(bit) for bit in enc_data])
    b = time.clock()
    print("Took",(b-a),"seconds")
