import time
from client import BlindstoreArray


if __name__ == '__main__':
    array = BlindstoreArray('http://localhost:5000/')
    print(array.length, array.record_size, array.index_length)
    start = time.time()
    print(array.retrieve(1))
    end = time.time()
    print('Retrieved in', end-start)
    print("Setting entry 1...")
    array.set(1, bytearray([2]))
    print("Retrieving entry 1...")
    print(array.retrieve(1))
