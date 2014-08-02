import json
import requests

def _get_db_size(url):
    r = requests.get(url + '/db_size')
    obj = json.loads(r.text)
    return obj['num_records'], obj['record_size']

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

URL = 'http://localhost:5000'

num_records, record_size = _get_db_size(URL)

print("The database has {0} records of {1} bits.".format(num_records, record_size))
print(_retrieve_from_server(URL, "antidisestablishmentarianism", "gobbledegookindex"))
print(_set_on_server(URL, "gobbledegookindex", "gobbledegookvalue"))
