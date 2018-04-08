from flask import Flask
from os.path import abspath, join, dirname


UPLOAD_FOLDER = abspath(join(dirname(__file__), 'static', 'uploaded_images'))
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

from app import routes