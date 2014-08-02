import json
import requests
import numpy as np

from pyscarab.scarab import EncryptedArray, EncryptedBit, \
    PrivateKey, PublicKey, generate_pair

def _retrieve_from_server(url, public_key, index):
    data = {
            'PUBLIC_KEY': public_key,
            'ENC_INDEX': index
            }
    r = requests.post(url + '/retrieve', data=data)
    return r.text

def _set_on_server(url, index, data):
    data = {
            'ENC_INDEX': index,
            'ENC_DATA': data
            }
    r = requests.post(url + '/set', data=data)
    return r.text

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
        enc_index = public_key.encrypt(_binary(index))

        data = { 'PUBLIC_KEY': str(public_key), 'ENC_INDEX': str(enc_index) }
        r = requests.post(self.url + 'retrieve', data=data)
        enc_data = [EncryptedBit(public_key, s) for s in json.loads(r.text)]
        return [secret_key.decrypt(bit) for bit in enc_data]

    def set(self, index, data):
        pass

if __name__ == '__main__':
    array = BlindstoreArray('http://localhost:5000/')
    print(array.length, array.record_size)
    print(array.retrieve(1))
