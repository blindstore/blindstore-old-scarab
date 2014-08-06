from functools import reduce
import numpy as np
from scarab import generate_pair, EncryptedArray
from common.utils import binary, index_length


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

    def __init__(self, record_size=3, record_count=5, database=None, fill=0):
        """
        Creates a new private store.
        :param record_size: the size of each record, in bits.
        :param record_count: the number of records that can be stored.
        :param database: numpy matrix of database values.
        """
        assert fill in [0, 1]
        if database is None:
            self.record_size = record_size
            self.record_count = record_count
            self.database = np.array([[fill] * record_size for _ in range(record_count)])
        else:
            self.record_count, self.record_size = database.shape
            self.database = database

        self.index_length = index_length(self.record_count)

    def retrieve2(self, cipher_query, public_key):
        """
        Optimized retrieve() method.

        - instead of XORing index bit, query bit and one (in gamma method), XOR query with negated index
        - precalculate {0, 1} XOR {each bit of query index} and construct gammas from these precomputed values

        This implementation performs 2*len(cipher_query) XORs to calculate all the gammas.

        Retrieves an encrypted record from the store, given a ciphered query.
        :param cipher_query: the encrypted index of the record to retrieve, as
                             an :class:`~EncryptedArray`
        :param public_key: the :class:`~PublicKey` to use.
        :raises ValueError: if the length of cipher_query does not equal the \
                            Store's index_length.
        """

        cipher_zro = public_key.encrypt(0)
        cipher_one = public_key.encrypt(1)

        precomputed = [
            [cipher_zro ^ x for x in cipher_query],  # 0
            [cipher_one ^ x for x in cipher_query]  # 1
        ]

        def func(x):
            x_bits = binary(x, size=self.index_length)
            # Take the XOR of the negated index bit and query bit
            gamma = [precomputed[1 - bit][i] for bit, i in zip(x_bits, range(len(x_bits)))]
            # TODO optimize the AND step
            # After all, we keep ANDing the same set of bits and the order is not important.
            return reduce(_AND, gamma)

        gammas = list(map(func, range(self.record_count)))
        gammas = np.array(gammas)

        # TODO: make this parallel
        return map(lambda x: _R(gammas, self.database[:, x], public_key), range(self.record_size))

    def retrieve(self, cipher_query, public_key):
        """
        Retrieves an encrypted record from the store, given a ciphered query.
        :param cipher_query: the encrypted index of the record to retrieve, as
                             an :class:`~EncryptedArray`
        :param public_key: the :class:`~PublicKey` to use.
        :raises ValueError: if the length of cipher_query does not equal the \
                            Store's index_length.
        """
        cipher_one = public_key.encrypt(1)

        def func(x):
            x = binary(x, size=self.index_length)
            x = public_key.encrypt(x)
            x = _gamma(cipher_query, x, cipher_one)
            return x

        # TODO: make this parallel
        gammas = map(func, range(self.record_count))
        gammas = np.array(list(gammas))

        # TODO: make this parallel
        return map(lambda x: _R(gammas, self.database[:, x], public_key), range(self.record_size))

    def set(self, idx, value):
        """
        Set a value in the array.
        :param idx: the unencrypted index to set.
        :param value: the unencrypted value.
        """
        if len(value) < self.record_size:
            padded_value = np.zeros(self.record_size, dtype=np.int)
            padded_value[padded_value.size - len(value):] = value
        else:
            padded_value = value

        self.database[idx] = padded_value


if __name__ == '__main__':
    store = Store(record_count=8, record_size=8)
    pk, sk = generate_pair()
    index = 2
    enc_data = store.retrieve(pk.encrypt(binary(index, size=store.index_length)), pk)
    print([sk.decrypt(bit) for bit in enc_data])
