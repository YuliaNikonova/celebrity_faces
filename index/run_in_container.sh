#!/bin/sh
export FLASK_APP=index.py
export CF_INDEX_SETTINGS=/index/docker_config
flask run --port=5002 --host=0.0.0.0