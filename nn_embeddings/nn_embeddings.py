from flask import request, Response, Flask

import os
import sys
import jsonpickle

sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

import image_processing
import signal

sess = None
print('Loading model...')
sess, images_placeholder, embeddings, phase_train_placeholder = image_processing.get_tf_session()
print('Model is loaded!')
app = Flask(__name__)


def handler(signal, frame):
    try:
        if sess is not None:
            sess.close()
    except Exception as e:
        print('Exception' + e)
    sys.exit(0)


signal.signal(signal.SIGINT, handler)
#signal.pause()


@app.route('/', methods=['POST'])
def upload_file():
    r = request
    # convert string of image data to uint8
    img = image_processing.load_image_from_request(r)
    aligned_img = image_processing.align_data([img])[0]
    vector = image_processing.get_vector(aligned_img, sess, images_placeholder, embeddings, phase_train_placeholder)
    #vector = aligned_img

    response = {'vector': vector.tolist()}
    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")
