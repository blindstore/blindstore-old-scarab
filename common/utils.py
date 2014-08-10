import math

import numpy as np
from scarab import EncryptedArray


def binary(num, size=32):
    """Binary representation of an integer as a list of 0, 1

    >>> binary(10, 8)
    [0, 0, 0, 0, 1, 0, 1, 0]

    :param num: integer
    :param size: size (pads with zeros)
    :return: the binary representation of num
    """
    ret = np.zeros(size, dtype=np.int)
    n = np.array([int(x) for x in list(bin(num)[2:])])
    ret[ret.size - n.size:] = n
    return ret


def index_bits(record_count):
    return math.ceil(math.log2(record_count))


def encrypt_index(pk, index, bits):
    """Encrypts the index for Blindstore query

    :param pk: PublicKey object
    :param index: index
    :param bits: number of bits to use for index
    """
    enc_ones = pk.encrypt([1] * bits)
    enc_index = pk.encrypt(binary(index, size=bits)) ^ enc_ones
    return enc_index
