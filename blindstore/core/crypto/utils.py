"""Cryptographic utils

.. note::

   Need to validate input for type and semantic correctness, since gmpy will
   segfault happily when something is wrong.

"""

import random
urandom = random.SystemRandom()

from contracts import contract, new_contract
from gmpy2 import mpz, mpz_random, random_state, is_odd


# Some cache
one = mpz(1)
two = mpz(2)

# Types and contracts
mpz_t = type(one)

new_contract('mpz', lambda s: isinstance(s, mpz_t))
new_contract('RandomState', lambda s: isinstance(s, RandomState))


class RandomState(object):

    """Random state wrapper object

    Because gmpy RandomState objects segfaults on every touch to it except
    when passed to mpz_random function.
    """

    @contract
    def __init__(self, seed=None):
        """Create gmpy random_state object using seed from /dev/urandom

        :type seed: None|int
        """
        max_seed_value = 10e+42
        if seed is None:
            seed = urandom.randint(0, max_seed_value)
        self.data = random_state(seed)


@contract
def random_mpz(a, b, rs=None):
    """Generate random mpz in range from a to b

    .. warning::

       Not thread-safe

    :param a: range start
    :type a: mpz
    :param b: range end
    :type b: mpz
    :param rs: random state
    :type rs: None|RandomState
    """
    if a >= b:
        raise ValueError('a should be less than b')

    # Create random state if not specified
    if rs is None:
        rs = RandomState()

    # mpz_random is not thread-safe
    return a + mpz_random(rs.data, (b - a))


@contract
def random_odd_mpz(a, b, rs=None):
    """Generate random odd mpz in range from a to b

    .. warning::

       Not thread-safe

    :param a: range start
    :type a: mpz
    :param b: range end
    :type b: mpz
    :param rs: random state
    :type rs: None|RandomState
    """
    if a >= b:
        raise ValueError('a should be less than b')

    # Create random state if not specified
    if rs is None:
        rs = RandomState()

    if not is_odd(a):
        a = a + 1
    if not is_odd(b):
        b = b - 1

    # mpz_random is not thread-safe
    return a + 2 * mpz_random(rs.data, (b - a) // 2)