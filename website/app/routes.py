from flask import render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from os.path import join, abspath
from app import app

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

'''
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')
'''

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
            '''return redirect(url_for('uploaded_file',
                                    filename=filename))'''
            return render_template('result.html')
    return render_template('index.html')


from flask import send_from_directory

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)