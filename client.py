import time
from client import BlindstoreArray

import scarab

from common.utils import encrypt_index


if __name__ == '__main__':
    array = BlindstoreArray('http://localhost:5000/')
    print('Records: {}, Size: {}, Bits: {}'.format(
        array.length, array.record_size, array.index_bits))

    start = time.clock()

    print(array.retrieve(1))
    print('Retrieved in', time.clock()-start, 'seconds')

    print("Setting entry 1...")
    array.set(1, bytearray([2]))
    print("Retrieving entry 1...")

    start = time.clock()
    print(array.retrieve(1))
    print('Retrieved in', time.clock()-start, 'seconds')
