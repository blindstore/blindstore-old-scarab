![logo](http://i.imgur.com/Yj5qUjm.png?1)

blindstore
==========

Blindstore server

Installation
------------

System requirements: [Python 3.4](https://python.org/), [numpy](https://numpy.org), [libscarab](https://github.com/blindstore/libScarab).

Python requirements:
```
$ pip install -r requirements.txt
```

Running a server
----------------

To run a Blindstore server, simply run `server.py` with Python 3.4.

To run the server in [Flask debug mode](http://flask.pocoo.org/docs/quickstart/#debug-mode), use the `--debug` switch. **Never** use this mode on a production machine, as it allows for remote code execution on the server.

Using the server from Python
----------------------------

A Python class for accessing a Blindstore server is provided. A simple example to connect, set and retrieve is shown below:

```python
from client import BlindstoreArray

URL = 'http://localhost:5000/'

array = BlindstoreArray(URL)

print("The Blindstore array has {count} entries of {size} bits each."
        .format(count=array.length, size=array.record_size))

print("Setting...")
array.set(2, bytearray([5]))

print("Retrieving...")
print(array.retrieve(2))
# -> [0, 1, 0, 1]
```

To connect to the server, we create a `BlindstoreArray` object, passing the server's URL. The `BlindstoreArray` object retrieves the number of records on the server, and the size (in bits) of each record, storing them in the `length` and `record_size` attributes respectively.

To store data on the server, we call the `set` method, passing the index to set as an `int` and the data as a byte array.

To retrieve data, simply call `retrieve` with the index. The data is returned as a list of bits.

Both `set` and `retrieve` calls are synchronous.

License
-------
[MIT License](http://opensource.org/licenses/MIT)

Credits
-------

Logo: 
* Eye designed by <a href="http://www.thenounproject.com/eugen.belyakoff">Eugen Belyakoff</a> from the <a href="http://www.thenounproject.com">Noun Project</a>.
* Inspiration – Devan Colley's [picture](http://devan-colley.deviantart.com/art/The-Eye-of-Providence-439920143)
