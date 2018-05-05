from flask import render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from os.path import join, abspath
import os
import requests
import json
from app import app



ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

EMBEDDING_SERVICE_URL = os.getenv('EMBEDDING_SERVICE_URL', 'http://127.0.0.1:5001/')
INDEX_SERVICE_URL = os.getenv('INDEX_SERVICE_URL', 'http://127.0.0.1:5002/')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_embedding_vector(filename):
    try:
        response = requests.post(EMBEDDING_SERVICE_URL, data=open(filename, 'rb').read())
        embedding_vector = response.json()['vector']
        return embedding_vector

    except Exception as e:
        print(e)
        return [1] * 128


def get_nearest_celeb_filename(embedding_vector):
    print('Get nearest vector')
    try:
        response = requests.post(INDEX_SERVICE_URL,
                                 data=json.dumps({'vector': embedding_vector}),
                                 headers={'content-type': 'application/json'})
        print(response.url)

        print(response.json())
        return response.json()['closest_celeb_filename']
    except Exception as e:
        print(e)
        return 'Aaron_Eckhart_0001.jpg'


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            print(abspath(join(app.config['UPLOAD_FOLDER'], filename)))
            file.save(join(app.config['UPLOAD_FOLDER'], filename))

            embedding_vector = get_embedding_vector(join(app.config['UPLOAD_FOLDER'], filename))

            closest_celeb_filename = get_nearest_celeb_filename(embedding_vector)

            return render_template('result.html',
                                   uploaded_filename=filename,
                                   celeb_filename='celeb_faces/' + closest_celeb_filename[:-4]+'.jpg')
    return render_template('index.html')


from flask import send_from_directory

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)