# used source code from https://github.com/davidsandberg/facenet

# MIT License
#
# Copyright (c) 2016 David Sandberg
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import cv2
from skimage.transform import resize
import numpy as np
from os.path import expanduser, join, abspath, basename
from os import listdir
import tensorflow as tf
import sys
import re


class FaceDetector():
    def detect_face(self, img):
        pass

class HoarOpenCVDetector(FaceDetector):
    def __init__(self, model_file):
        self.face_cascade = cv2.CascadeClassifier(model_file)

    def detect_face(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        scale = 0.15
        for (x, y, w, h) in faces:
            x_min = x - int(scale * w)
            y_min = y - int(scale * h)
            x_max = x + w + int(scale * w)
            y_max = y + h + int(scale * h)
            return img[x_min:x_max, y_min:y_max, :]


# from facenet
def prewhiten(x):
    mean = np.mean(x)
    std = np.std(x)
    std_adj = np.maximum(std, 1.0/np.sqrt(x.size))
    y = np.multiply(np.subtract(x, mean), 1/std_adj)
    return y

# from facenet
def get_model_filenames(model_dir):
    files = listdir(model_dir)
    meta_files = [s for s in files if s.endswith('.meta')]
    if len(meta_files)==0:
        raise ValueError('No meta file found in the model directory (%s)' % model_dir)
    elif len(meta_files)>1:
        raise ValueError('There should not be more than one meta file in the model directory (%s)' % model_dir)
    meta_file = meta_files[0]
    ckpt = tf.train.get_checkpoint_state(model_dir)
    if ckpt and ckpt.model_checkpoint_path:
        ckpt_file = basename(ckpt.model_checkpoint_path)
        return meta_file, ckpt_file

    meta_files = [s for s in files if '.ckpt' in s]
    max_step = -1
    for f in files:
        step_str = re.match(r'(^model-[\w\- ]+.ckpt-(\d+))', f)
        if step_str is not None and len(step_str.groups())>=2:
            step = int(step_str.groups()[1])
            if step > max_step:
                max_step = step
                ckpt_file = step_str.groups()[0]
    return meta_file, ckpt_file


def prepocess_image(img, face_detector, image_size=160):
    img = face_detector.detect_face(img)
    img = prewhiten(img)
    img = resize(img, (image_size, image_size))
    return img


def get_tf_session(model_directory):
    sess = tf.Session()
    meta_file, ckpt_file = get_model_filenames(model_directory)
    saver = tf.train.import_meta_graph(join(model_directory, meta_file))
    saver.restore(sess, join(model_directory, ckpt_file))
    images_placeholder = tf.get_default_graph().get_tensor_by_name("input:0")
    embeddings = tf.get_default_graph().get_tensor_by_name("embeddings:0")
    phase_train_placeholder = tf.get_default_graph().get_tensor_by_name("phase_train:0")
    return sess, images_placeholder, embeddings, phase_train_placeholder


def get_vector(image, sess, images_placeholder, embeddings, phase_train_placeholder):
    feed_dict = {images_placeholder: [image], phase_train_placeholder: False}
    return sess.run(embeddings, feed_dict=feed_dict)[0]

