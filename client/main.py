import json
import requests
import numpy as np
import base64

from scarab import EncryptedArray, EncryptedBit, \
    PrivateKey, PublicKey, generate_pair

from common.utils import binary

try:
    import bs_demo
except ImportError:
    import sys
    print("Warning: no logging defined", file=sys.stderr)
    demo_logger = None
else:
    demo_logger = bs_demo.DemoClient('http://localhost:3000')

def demo_log(title, message):
    if demo_logger is not None:
        demo_logger.client_msg(title, message)

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

        demo_log('Ask for DB metadata', '')

        r = requests.get(self.url + 'db_size')
        obj = json.loads(r.text)
        self.length = obj['num_records']
        self.record_size = obj['record_size']
        self.index_length = obj['index_length']

        demo_log('Received DB metadata',
                 'Record size: {}, Number of records: {}, Index length: {}'.format(
                     self.record_size, self.length, self.index_length)
        )

    def retrieve(self, index):
        """
        Retrieves a value from the Blindstore array.
        :param index: the index of the value to retrieve.
        :returns: the value stored at the given index, as a bit array.
        """
        demo_log('Prepare request of a DB entry: generate keys',
                 'Will ask for row #{}.'.format(index))
        public_key, secret_key = generate_pair()
        demo_log('Keys created',
                 'Done with the encryption keys generation.'.format(
                     self.record_size, self.length))
        enc_index = public_key.encrypt(binary(index, size=self.index_length), secret_key)
        demo_log('Index encrypted and sent to server',
                 'Encrypted index: {}.'.format(str(enc_index)))
        data = {'PUBLIC_KEY': str(public_key), 'ENC_INDEX': str(enc_index)}
        r = requests.post(self.url + 'retrieve', data=data)
        enc_data = [EncryptedBit(public_key, str(s)) for s in json.loads(r.text)]
        demo_log('Got response to DB query', str([str(x) for x in enc_data]))

        ret =  [secret_key.decrypt(bit) for bit in enc_data]
        demo_log('Response decrypted. DB entry #{} is'.format(index), str(ret))
        return ret

    def set(self, index, data):
        """
        Set a value in the Blindstore array.
        :param index: int -- the index of the row to set.
        :param data: byte string -- the byte string to store at the location.
        """
        demo_log('Sent request to update a DB entry', 'Setting row number {} to {}.'
                 .format(index, data))
        data = {'INDEX': str(index), 'DATA': base64.b64encode(data)}
        r = requests.post(self.url + 'set', data=data)
