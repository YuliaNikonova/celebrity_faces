import os
import sys
import numpy as np
from os.path import abspath, dirname, join
from tqdm import trange

FACENET_SRC_DIR = os.getenv('FACENET_SRC_DIR',
                            abspath(join(dirname(__file__), 'facenet_src')))
sys.path.append(FACENET_SRC_DIR)
PAIRS_PATH = os.getenv('PAIRS_PATH',
                       abspath(join(abspath(dirname(abspath(dirname(__file__)))), 'data', 'pairs.txt')))



LFW_RAW_PATH = os.getenv('LFW_RAW_PATH',
                         abspath(join(abspath(dirname(abspath(dirname(__file__)))), 'data', 'lfw_raw')))

from image_processing import *

from lfw import get_paths, read_pairs, evaluate


def test_nn():
    pairs = read_pairs(PAIRS_PATH)
    paths, actual_issame = get_paths(LFW_RAW_PATH, pairs)

    print('Loading nets for face detection...')

    pnet, rnet, onet = get_face_detect_nets()

    print('Loading images...')

    original_images = [load_image_from_file(path) for path in paths]

    print('Aligning images...')
    aligned_images = align_data(original_images, pnet, rnet, onet)

    nrof_images = len(aligned_images)
    batch_size = 100
    nrof_batches = nrof_images // batch_size

    print('Loading net for embeddings...')
    sess, images_placeholder, embeddings, phase_train_placeholder = get_tf_session()

    try:

        embedding_size = embeddings.get_shape()[1]
        emb_array = np.zeros((nrof_images, embedding_size))

        print('Calculating embeddings...')

        for i in trange(nrof_batches):
            start_index = i * batch_size
            end_index = min((i + 1) * batch_size, nrof_images)
            images_batch = aligned_images[start_index:end_index]
            feed_dict = {images_placeholder: images_batch, phase_train_placeholder: False}
            emb_array[start_index:end_index, :] = sess.run(embeddings, feed_dict=feed_dict)

        print('Evaluating...')
        tpr, fpr, accuracy, val, val_std, far = evaluate(emb_array,
                                                         actual_issame,
                                                         nrof_folds=10,
                                                         distance_metric=1,
                                                         subtract_mean=True)

        print('Accuracy: %2.5f+-%2.5f' % (np.mean(accuracy), np.std(accuracy)))
        print('Validation rate: %2.5f+-%2.5f @ FAR=%2.5f' % (val, val_std, far))
    except Exception as e:
        print("Error " + e)

    finally:
        sess.close()


if __name__ == "__main__":
    test_nn()
