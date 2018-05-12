#!/bin/sh
export FLASK_APP=index.py
export FLASK_DEBUG=0
flask run --port=5002 --host=0.0.0.0