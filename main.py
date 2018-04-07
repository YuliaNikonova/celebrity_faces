from annoy import AnnoyIndex
import numpy as np
from scipy import misc
from os.path import expanduser, join, abspath
MODEL_DIR = abspath(join(expanduser('~'), 'models', 'facenet', '20170512-110547'))
from image_processing import prepocess_image, get_tf_session, get_vector

INDEX_FILENAME = 'data/index.ann'
PATHS_NPY = 'data/paths.npy'
EMBEDDING_NPY = 'data/embeddings.npy'

PATHS = np.load(PATHS_NPY)


def build_index(embeddings):
    dim = embeddings.shape[1]
    u = AnnoyIndex(dim)
    try:
        u.load(INDEX_FILENAME)
        print("Index loaded")
    except FileNotFoundError:
        print('Building index...')
        for index, vector in enumerate(embeddings):
            if index % 500 == 0:
                print("{} vectors added".format(index))
            u.add_item(index, vector)
            u.build(10)  # 10 trees
            u.save(INDEX_FILENAME)

            u = AnnoyIndex(dim)
            u.load(INDEX_FILENAME)
    return u


def main():
    embeddings = np.load(EMBEDDING_NPY)
    index = build_index(embeddings)

    test_filename = abspath(join(expanduser('~'), 'datasets', 'lfw', 'raw', 'Aaron_Eckhart', 'Aaron_Eckhart_0001.jpg'))
    image = misc.imread(test_filename)
    img_preprocessed = prepocess_image(image)

    sess, images_placeholder, embeddings, phase_train_placeholder = get_tf_session(MODEL_DIR)
    try:
        vector = get_vector(img_preprocessed, sess, images_placeholder, embeddings, phase_train_placeholder)

        closest_celeb_index = index.get_nns_by_vector(vector, 1)[0]
        closest_celeb_path = PATHS[closest_celeb_index]
        print(closest_celeb_path)
    finally:
        sess.close()



if __name__ == "__main__":
    # execute only if run as a script
    main()
