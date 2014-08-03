import base64
import json
import struct

from flask import Flask, request
from scarab import EncryptedArray, PublicKey

from .store import Store
from common.utils import binary


app = Flask(__name__)

store = Store()

@app.route('/db_size')
def get_db_size():
    data = {'num_records': store.record_count, 'record_size': store.record_size}
    return json.dumps(data), 200, {'Content-Type': 'text/json'}


@app.route('/retrieve', methods=['POST'])
def retrieve():
    print("Starting retrieve call...")
    public_key = PublicKey(str(request.form['PUBLIC_KEY']))

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
        return '', 200
    except Exception as e:
        #import traceback
        #traceback.print_last()
        print(e)
