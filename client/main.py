import json
import requests
import numpy as np
import base64

from scarab import EncryptedArray, EncryptedBit, \
    PrivateKey, PublicKey, generate_pair

from common.utils import binary, encrypt_index


class BlindstoreArray:
    """
    Class for connecting to a Blindstore array over the network.
    """

    def __init__(self, url):
        """
        Creates a new BlindstoreArray.
        :param url: the URL of the server to connect to.
        """
        self.url = url if url.endswith('/') else url + '/'
        self.get_db_size()

    def get_db_size(self):
        """
        Get the size of the Blindstore array on the server.
        :returns: a tuple containing the number of records followed by the
                  size of each record, in bits.
        """
        r = requests.get(self.url + 'db_size')
        obj = json.loads(r.text)
        self.length = obj['num_records']
        self.record_size = obj['record_size']
        self.index_bits = obj['index_bits']

    def retrieve(self, index):
        """
        Retrieves a value from the Blindstore array.
        :param index: the index of the value to retrieve.
        :returns: the value stored at the given index, as a bit array.
        """
        public_key, secret_key = generate_pair()
        enc_index = encrypt_index(public_key, index, self.index_bits)

        data = {'PUBLIC_KEY': str(public_key), 'ENC_INDEX': str(enc_index)}
        r = requests.post(self.url + 'retrieve', data=data)
        enc_data = [EncryptedBit(public_key, str(s)) \
            for s in json.loads(r.text)]
        return [secret_key.decrypt(bit) for bit in enc_data]

    def set(self, index, data):
        """
        Set a value in the Blindstore array.
        :param index: int -- the index of the row to set.
        :param data: byte string -- the byte string to store at the location.
        """
        data = {'INDEX': str(index), 'DATA': base64.b64encode(data)}
        r = requests.post(self.url + 'set', data=data)
