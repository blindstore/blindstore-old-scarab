from functools import reduce
import random
import numpy as np
from common.utils import binary, index_length
from server.cached_reducer import CachedReducer


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


def _R(gammas, column, enc_zero):
    """
    Calculates the value of R() function, as described in PDF (paragraph 3.1.3)
    :param gammas: gammas
    :param column: column
    :param enc_zero: encrypted zero
    :return: the value of the R function
    """
    return reduce(_XOR, gammas[np.where(column == 1)], enc_zero)


class Store:
    """A private store."""

    def __init__(self, record_size=3, record_count=5, database=None, fill=0):
        """
        Creates a new private store.
        :param record_size: the size of each record, in bits.
        :param record_count: the number of records that can be stored.
        :param database: numpy matrix of database values.
        :param fill: value to fill the database with.
        """
        if database is None:
            if fill == 'random':
                arr = [[random.randint(0, 1) for _ in range(record_size)] for _ in range(record_count)]
            else:
                arr = [[fill] * record_size for _ in range(record_count)]
            database = np.array(arr)
        self.record_count, self.record_size = database.shape
        self.database = database
        self.index_length = index_length(self.record_count)

    def retrieve2(self, cipher_query, public_key):
        """
        Retrieves an encrypted record from the store, given a ciphered query.
        FHE operation results are now cached to speed up computation.
        :param cipher_query: the encrypted index of the record to retrieve, as
                             an :class:`~EncryptedArray`
        :param public_key: the :class:`~PublicKey` to use.
        :raises ValueError: if the length of cipher_query does not equal the \
                            Store's index_length.
        """
        cipher_zro = public_key.encrypt(0)
        cipher_one = public_key.encrypt(1)

        precomputed = [
            [x for x in cipher_query],  # 0
            [cipher_one ^ x for x in cipher_query]  # 1
        ]

        gamma_reducer = CachedReducer(_AND)  # must be instantiated separately for each thread

        def func_gamma(x):
            x_bits = binary(x, size=self.index_length)
            # Take the XOR of the negated index bit and query bit
            gamma = [precomputed[1 - bit][i] for bit, i in zip(x_bits, range(len(x_bits)))]
            return gamma_reducer.reduce(gamma)

        gammas = list(map(func_gamma, range(self.record_count)))
        gammas = np.array(gammas)

        r_reducer = CachedReducer(_XOR)  # must be instantiated separately for each thread

        def func_r(x):
            column = self.database[:, x]
            return r_reducer.reduce(gammas[np.where(column == 1)], cipher_zro)

        return list(map(func_r, range(self.record_size)))

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
        cipher_zro = public_key.encrypt(0)

        def func(x):
            x = binary(x, size=self.index_length)
            x = public_key.encrypt(x)
            x = _gamma(cipher_query, x, cipher_one)
            return x

        # TODO: make this parallel
        gammas = map(func, range(self.record_count))
        gammas = np.array(list(gammas))

        # TODO: make this parallel
        return list(map(lambda x: _R(gammas, self.database[:, x], cipher_zro), range(self.record_size)))

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
