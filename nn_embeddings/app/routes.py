from flask import render_template, request, redirect, url_for, flash, Response
from werkzeug.utils import secure_filename
from os.path import join, abspath
import io
import jsonpickle
import numpy as np
import cv2
from app import app, hoar_face_detector, sess, images_placeholder, embeddings, phase_train_placeholder
from app import image_processing
from json import dumps

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['POST'])
def upload_file():
    r = request
    # convert string of image data to uint8
    img = cv2.imdecode(np.fromstring(r.data, np.uint8), cv2.IMREAD_COLOR)
    print(img.shape)
    img_preprocessed = image_processing.prepocess_image(img, hoar_face_detector)
    #print(img_preprocessed)
    response = {'vector':
                    image_processing.get_vector(img_preprocessed, sess, images_placeholder, embeddings, phase_train_placeholder).tolist()}
    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")

