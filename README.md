blindstore
==========

Blindstore server

Installation
------------

System requirements: [numpy](https://numpy.org), [libscarab](https://github.com/blindstore/libScarab).

Python requirements:
```
pip install -r requirements.txt
```

Running
-------

To run a Blindstore server, simply run `server.py` with Python 3.4.

To run the server in [Flask debug mode](http://flask.pocoo.org/docs/quickstart/#debug-mode), use the `--debug` switch. **Never** use this mode on a production machine, as it allows for remote code execution on the server.
