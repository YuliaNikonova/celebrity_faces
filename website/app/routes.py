from flask import render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from os.path import join, abspath
import requests
import json
from app import app



ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

VECTOR_URL = 'http://127.0.0.1:5001/'
INDEX_URL = 'http://127.0.0.1:5002/'


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


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
            response = requests.post(VECTOR_URL, data=open(join(app.config['UPLOAD_FOLDER'], filename), 'rb').read())
            embedding_vector = response.json()['vector']
            print(embedding_vector)
            '''return redirect(url_for('uploaded_file',
                                    filename=filename))'''


            response = requests.post(INDEX_URL,
                                     data=json.dumps({'vector': embedding_vector}),
                                     headers={'content-type': 'application/json'})

            print(response.json())
            closest_celeb_filename = response.json()['closest_celeb_filename']
            return render_template('result.html',
                                   uploaded_filename=filename,
                                   celeb_filename='celeb_faces/' + closest_celeb_filename[:-4]+'.jpg')
    return render_template('index.html')


from flask import send_from_directory

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)