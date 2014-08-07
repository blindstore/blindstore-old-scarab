import numpy as np

from nose.tools import *

from scarab import generate_pair

from server.store import Store
from common.utils import binary

RECORD_COUNT = 8
RECORD_SIZE = 8

class TestStore(object):
    def setup(self):
        self.db = np.array([[1] * min(RECORD_SIZE, x) + [0] * max(0, RECORD_SIZE - x) for x in range(RECORD_COUNT)])
        self.store = Store(database=self.db)

    def test_retrieve(self):
        public_key, secret_key = generate_pair()
        index = 2
        enc_index = public_key.encrypt(binary(index, size=self.store.index_blength))
        enc_data = self.store.retrieve(enc_index, public_key)
        data = [secret_key.decrypt(bit) for bit in enc_data]
        assert_true(all(data == self.db[index]))

    def test_set(self):
        index = 2
        new_value = [0, 0, 0, 0, 1, 1, 1, 1]
        self.store.set(index, new_value)

        public_key, secret_key = generate_pair()
        enc_index = public_key.encrypt(binary(index, size=self.store.index_blength))
        enc_data = self.store.retrieve(enc_index, public_key)
        data = [secret_key.decrypt(bit) for bit in enc_data]
        assert_equals(data, new_value)

