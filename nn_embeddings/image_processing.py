import os
import sys
import tensorflow as tf
import numpy as np
from scipy import misc
from tqdm import tqdm
import imageio

FACENET_SRC_DIR = os.getenv('FACENET_SRC_DIR',
                            os.path.abspath(os.path.join(os.path.dirname(__file__), 'facenet_src')))
sys.path.append(FACENET_SRC_DIR)
import align.detect_face
from facenet import get_model_filenames, prewhiten

MODEL_DIR = os.getenv('MODEL_DIR',
                      os.path.abspath(os.path.join(os.path.dirname(__file__), 'models', '20170512-110547')))


def get_face_detect_nets():
    with tf.Graph().as_default():
        sess = tf.Session()
        with sess.as_default():
            pnet, rnet, onet = align.detect_face.create_mtcnn(sess, None)
    return pnet, rnet, onet


def load_image_from_file(filepath):
    return imageio.imread(filepath)


def load_image_from_request(request):
    return imageio.imread(request.data)


PNET, RNET, ONET = get_face_detect_nets()





def align_data(original_images, pnet=PNET, rnet=RNET, onet=ONET, image_size=160, margin=44):
    minsize = 20  # minimum size of face
    threshold = [0.6, 0.7, 0.7]  # three steps's threshold
    factor = 0.709  # scale factor
    img_list = []
    for img in tqdm(original_images):
        img_size = np.asarray(img.shape)[0:2]
        bounding_boxes, _ = align.detect_face.detect_face(img, minsize, pnet, rnet, onet, threshold, factor)
        if len(bounding_boxes) < 1:
            continue
        det = np.squeeze(bounding_boxes[0, 0:4])
        bb = np.zeros(4, dtype=np.int32)
        bb[0] = np.maximum(det[0] - margin / 2, 0)
        bb[1] = np.maximum(det[1] - margin / 2, 0)
        bb[2] = np.minimum(det[2] + margin / 2, img_size[1])
        bb[3] = np.minimum(det[3] + margin / 2, img_size[0])
        cropped = img[bb[1]:bb[3], bb[0]:bb[2], :]
        aligned = misc.imresize(cropped, (image_size, image_size), interp='bilinear')
        prewhitened = prewhiten(aligned)
        img_list.append(prewhitened)
    images = np.stack(img_list)
    return images


def get_tf_session(model_directory=MODEL_DIR):
    sess = tf.Session()
    meta_file, ckpt_file = get_model_filenames(model_directory)
    saver = tf.train.import_meta_graph(os.path.join(model_directory, meta_file))
    saver.restore(sess, os.path.join(model_directory, ckpt_file))
    images_placeholder = tf.get_default_graph().get_tensor_by_name("input:0")
    embeddings = tf.get_default_graph().get_tensor_by_name("embeddings:0")
    phase_train_placeholder = tf.get_default_graph().get_tensor_by_name("phase_train:0")
    return sess, images_placeholder, embeddings, phase_train_placeholder


def get_vector(image, sess, images_placeholder, embeddings, phase_train_placeholder):
    feed_dict = {images_placeholder: [image], phase_train_placeholder: False}
    return sess.run(embeddings, feed_dict=feed_dict)[0]