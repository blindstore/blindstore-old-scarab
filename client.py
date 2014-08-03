from client import BlindstoreArray


if __name__ == '__main__':
    array = BlindstoreArray('http://localhost:5000/')
    print(array.length, array.record_size)
    print(array.retrieve(1))
    print("Setting entry 1...")
    array.set(1, bytearray([2]))
    print("Retrieving entry 1...")
    print(array.retrieve(1))
