#!/bin/sh
export FLASK_APP=website.py
FLASK_DEBUG=1
flask run --port=5000 --host=0.0.0.0