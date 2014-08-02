import argparse
import json

from flask import Flask, request

parser = argparse.ArgumentParser(description="Start a Blindstore server.")
parser.add_argument('-d', '--debug', action='store_true',
                    help="enable Flask debug mode. DO NOT use in production.")
args = parser.parse_args()

NUM_RECORDS = 5
RECORD_SIZE = 64

app = Flask(__name__)

@app.route('/db_size')
def get_db_size():
    return json.dumps({'num_records': NUM_RECORDS, 'record_size': RECORD_SIZE}), \
           200, {'Content-Type': 'text/json'}

@app.route('/retrieve', methods=['POST'])
def get():
    public_key = request.form['PUBLIC_KEY']
    enc_index  = request.form['ENC_INDEX']

    return "/retrieve index '{index}' with key '{key}'".format(index=enc_index, key=public_key)

@app.route('/set', methods=['POST'])
def put():
    enc_index = request.form['ENC_INDEX']
    enc_data  = request.form['ENC_DATA']

    return "/set '{index}' to '{data}'".format(data=enc_data, index=enc_index)

if __name__ == '__main__':
    app.run(debug=args.debug)
