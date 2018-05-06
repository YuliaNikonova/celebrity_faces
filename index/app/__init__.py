from annoy import AnnoyIndex
import numpy as np
from flask import Flask
from os.path import expanduser, join, abspath

MODEL_DIR = abspath(join(expanduser('~'), 'models', 'facenet', '20170512-110547'))


INDEX_FILENAME = abspath(join(expanduser('~'), 'repos', 'celebrity_faces', 'data', 'index.ann'))
PATHS_NPY = abspath(join(expanduser('~'), 'repos', 'celebrity_faces', 'data', 'paths.npy')) #'data/paths.npy'
EMBEDDING_NPY = abspath(join(expanduser('~'), 'repos', 'celebrity_faces', 'data', 'embeddings.npy'))


print(EMBEDDING_NPY)

PATHS = np.load(PATHS_NPY)
embeddings = np.load(EMBEDDING_NPY)

dim = embeddings.shape[1]
embedding_index = AnnoyIndex(dim)
try:
    embedding_index.load(INDEX_FILENAME)
    print("Index loaded")
except FileNotFoundError:
    print('Building index...')
    for index, vector in enumerate(embeddings):
        if index % 500 == 0:
            print("{} vectors added".format(index))
        embedding_index.add_item(index, vector)
        embedding_index.build(10)  # 10 trees
        embedding_index.save(INDEX_FILENAME)

        embedding_index = AnnoyIndex(dim)
        embedding_index.load(INDEX_FILENAME)


app = Flask(__name__)

from app import routes