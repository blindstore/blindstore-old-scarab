from functools import reduce
import numpy as np

from pyscarab.scarab import generate_pair

_ADD = lambda a, b: a + b
_MUL = lambda a, b: a * b
_AND = lambda a, b: a & b
_XOR = lambda a, b: a ^ b


def _binary(num, size=32):
    """Binary representation of an integer as a list of 0, 1

    >>> binary(10, 8)
    [0, 0, 0, 0, 1, 0, 1, 0]

    :param num:
    :param size: size (pads with zeros)
    :return: the binary representation of num
    """
    ret = np.zeros(size, dtype=np.int)
    n = np.array([int(x) for x in list(bin(num)[2:])])
    ret[ret.size - n.size:] = n
    return ret


def _gamma(cq, ci, co):
    """
    Calculates the value of the gamma function, as described in PDF (paragraph 3.1.2)
    :param cq: cipher query
    :param ci: cipher index
    :param co: cipher one
    :return: the value of the gamma function
    """
    return reduce(_AND, [a ^ b ^ co for a, b in zip(cq, ci)])


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
    def __init__(self):
        self.record_size = 3
        self.record_count = 5
        self.database = np.array(
            [[1] * min(self.record_size, x) + [0] * max(0, self.record_size - x) for x in range(self.record_count)])

    def retrieve(self, cipher_query, public_key):
        indices = [_binary(x) for x in range(self.record_count)]
        cipher_indices = [public_key.encrypt(index) for index in indices]
        cipher_one = public_key.encrypt(1)
        gammas = np.array([_gamma(cipher_query, ci, cipher_one) for ci in cipher_indices])

        tmp = []
        for c in range(self.record_size):
            column = self.database[:, c]
            tmp.append(_R(gammas, column, public_key))

        return tmp


if __name__ == '__main__':
    store = Store()
    pk, sk = generate_pair()
    index = 2
    enc_data = store.retrieve(pk.encrypt(binary(index)), pk)
    print(store.database)
    print([sk.decrypt(bit) for bit in enc_data])
