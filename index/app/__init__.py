from annoy import AnnoyIndex
from flask import Flask
from os.path import expanduser, join, abspath
from os import environ
import json


app = Flask(__name__)
app.config.from_pyfile('default_config')
if environ.get('CF_INDEX_SETTINGS') is not None:
    app.config.from_envvar('CF_INDEX_SETTINGS')

INDEX_FILENAME = app.config['INDEX_FILENAME']
PATHS_JSON = app.config['PATHS_JSON']
EMBEDDING_JSON = app.config['EMBEDDING_JSON']




with open(PATHS_JSON, 'r') as fp:
    PATHS = json.load(fp)

with open(EMBEDDING_JSON, 'r') as fp:
    embeddings = json.load(fp)


'''
PATHS = np.load(PATHS_NPY)
embeddings = np.load(EMBEDDING_NPY)
'''

dim = len(embeddings[0])
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




from app import routes