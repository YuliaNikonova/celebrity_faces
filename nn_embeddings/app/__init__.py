from flask import Flask
from os.path import abspath, join, dirname

from  app import image_processing #import get_tf_session, HoarOpenCVDetector



app = Flask(__name__)
app.config['FACENET_MODEL_DIR'] = join(dirname(__file__), 'models', '20170512-110547')
app.config['FACE_DETECTOR_MODEL_FILE'] = join(dirname(__file__), 'models', 'haarcascades', 'haarcascade_frontalface_default.xml')



sess, images_placeholder, embeddings, phase_train_placeholder = image_processing.get_tf_session(app.config['FACENET_MODEL_DIR'])
hoar_face_detector = image_processing.HoarOpenCVDetector(app.config['FACE_DETECTOR_MODEL_FILE'])


from app import routes

