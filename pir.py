from functools import reduce
import numpy as np
import time
from scarab import EncryptedArray, EncryptedBit, \
    PrivateKey, PublicKey, generate_pair

_ADD = lambda a, b: a + b
_MUL = lambda a, b: a * b
_AND = lambda a, b: a & b
_XOR = lambda a, b: a ^ b

pk, sk = None, None


def binary(num, size=32):
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


def gamma(cq, ci, co):
    """
    Calculates the value of the gamma function, as described in PDF (paragraph 3.1.2)
    :param cq: cipher query
    :param ci: cipher index
    :param co: cipher one
    :return: the value of the gamma function
    """
    return reduce(_AND, [a ^ b ^ co for a, b in zip(cq, ci)])


def R(gammas, column, public_key):
    """
    Calculates the value of R() function, as described in PDF (paragraph 3.1.3)
    :param gammas: gammas
    :param column: column
    :param public_key: public key
    :return: the value of the R function
    """
    return reduce(_XOR, gammas[np.where(column == 1)], public_key.encrypt(0))

# #######
RECORD_SIZE = 3
RECORD_COUNT = 5
database = np.array([[1] * min(RECORD_SIZE, x) + [0] * max(0, RECORD_SIZE - x) for x in range(RECORD_COUNT)])
########


def server_generate_response(cipher_query, pk):
    indices = [binary(x) for x in range(RECORD_COUNT)]
    cipher_indices = [pk.encrypt(index) for index in indices]
    cipher_one = pk.encrypt(1)
    gammas = np.array([gamma(cipher_query, ci, cipher_one) for ci in cipher_indices])
    tmp = []
    for c in range(RECORD_SIZE):
        foobar = database[:, c]
        tmp.append(R(gammas, foobar, pk))
    return np.array(tmp)

def serialize_and_deserialize(cipher_query, public_key):
    serialized_query = str(cipher_query)
    serialized_public_key = str(public_key)
    deserialized_public_key = PublicKey(serialized_public_key)
    deserialized_query = EncryptedArray(len(cipher_query), deserialized_public_key, serialized_query)
    enc_data = server_generate_response(deserialized_query, deserialized_public_key)
    s_bits = [str(bit) for bit in enc_data]
    deserialized_enc_data = [EncryptedBit(public_key, bit) for bit in s_bits]
    return deserialized_enc_data

def client_perform_query(i):
    response = serialize_and_deserialize(pk.encrypt(binary(i)), pk)
    result = [sk.decrypt(r) for r in response]
    return result

########
########
########

if __name__ == '__main__':
    print('Database size:', RECORD_COUNT, 'x', RECORD_SIZE)

    a = time.clock()
    pk, sk = generate_pair()
    b = time.clock()
    print('keys were generated in', (b - a), 'seconds')

    a = time.clock()
    row = client_perform_query(1)
    b = time.clock()
    print('response generated in', (b - a), 'seconds')

    print(row)
