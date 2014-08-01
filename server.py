from flask import Flask, request

app = Flask(__name__)

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
    app.run(debug=True)
