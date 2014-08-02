import argparse
import json
from flask import Flask, request
from pyscarab.scarab import EncryptedArray, PublicKey
from store import Store


parser = argparse.ArgumentParser(description="Start a Blindstore server.")
parser.add_argument('-d', '--debug', action='store_true',
                    help="enable Flask debug mode. DO NOT use in production.")
args = parser.parse_args()

NUM_RECORDS = 5
RECORD_SIZE = 64

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
def put():
    pk = None
    enc_index = EncryptedArray(request.form['ENC_INDEX'], pk)
    enc_data = EncryptedArray(request.form['ENC_DATA'], pk)

    return "/set '{index}' to '{data}'".format(data=enc_data, index=enc_index)


if __name__ == '__main__':
    app.run(debug=args.debug)
