import json
import requests
import numpy as np
import base64

from pyscarab.scarab import EncryptedArray, EncryptedBit, \
    PrivateKey, PublicKey, generate_pair

from utils import binary


class BlindstoreArray:
    def __init__(self, url):
        self.url = url if url.endswith('/') else url + '/'
        self.length, self.record_size = self.get_db_size()

    def get_db_size(self):
        r = requests.get(self.url + 'db_size')
        obj = json.loads(r.text)
        return obj['num_records'], obj['record_size']

    def retrieve(self, index):
        public_key, secret_key = generate_pair()
        enc_index = public_key.encrypt(binary(index))

        data = {'PUBLIC_KEY': str(public_key), 'ENC_INDEX': str(enc_index)}
        r = requests.post(self.url + 'retrieve', data=data)
        enc_data = [EncryptedBit(public_key, s) for s in json.loads(r.text)]
        return [secret_key.decrypt(bit) for bit in enc_data]

    def set(self, index, data):
        # data: byte string
        data = {'INDEX': str(index), 'DATA': base64.b64encode(data)}
        r = requests.post(self.url + 'set', data=data)


if __name__ == '__main__':
    array = BlindstoreArray('http://localhost:5000/')
    print(array.length, array.record_size)
    print(array.retrieve(1))
    print("Setting entry 1...")
    array.set(1, bytearray([2]))
    print("Retrieving entry 1...")
    print(array.retrieve(1))
