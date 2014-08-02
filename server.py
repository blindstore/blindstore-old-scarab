import argparse
import base64
import json
import struct

from flask import Flask, request
from pyscarab.scarab import EncryptedArray, PublicKey
from utils import binary
from store import Store


parser = argparse.ArgumentParser(description="Start a Blindstore server.")
parser.add_argument('-d', '--debug', action='store_true',
                    help="enable Flask debug mode. DO NOT use in production.")
args = parser.parse_args()

NUM_RECORDS = 5
RECORD_SIZE = 64

def _bytes_to_int(byte_string):
    struct.unpack('<L', byte_string)

app = Flask(__name__)

store = Store()

@app.route('/db_size')
def get_db_size():
    return json.dumps({'num_records': NUM_RECORDS, 'record_size': RECORD_SIZE}), \
        200, {'Content-Type': 'text/json'}


@app.route('/retrieve', methods=['POST'])
def retrieve():
    print("Starting retrieve call...")
    public_key = PublicKey(request.form['PUBLIC_KEY'])

    enc_index = EncryptedArray(store.record_size, public_key, request.form['ENC_INDEX'])
    enc_data = store.retrieve(enc_index, public_key)
    s_bits = [str(b) for b in enc_data]
    obj = json.dumps(s_bits)

    return obj


@app.route('/set', methods=['POST'])
def set():
    try:
        index = int(request.form['INDEX'])
        data = int.from_bytes(base64.b64decode(request.form['DATA']), 'big')

        store.set(index, binary(data, store.record_size))
        return None, 200
    except Exception as e:
        #import traceback
        #traceback.print_last()
        print(e)


if __name__ == '__main__':
    app.run(debug=args.debug)
