#!/bin/sh
export FLASK_APP=nn_embeddings.py
export FLASK_DEBUG=0
flask run --port=5001 --host=0.0.0.0