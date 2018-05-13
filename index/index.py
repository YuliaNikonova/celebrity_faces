from annoy import AnnoyIndex
from flask import Flask, request, Response
from os.path import dirname, join, abspath
from os import getenv
import json
import jsonpickle

from python.index import PyNode, PyDistance_l1, PyDistance_l2, PyNSW

INDEX_FILENAME = getenv('INDEX_FILENAME',
                      abspath(join(abspath(dirname(abspath(dirname(__file__)))), 'data', 'index.ann')))
PATHS_JSON = getenv('PATHS_JSON',
                      abspath(join(abspath(dirname(abspath(dirname(__file__)))), 'data', 'paths.json')))
EMBEDDING_JSON = getenv('EMBEDDING_JSON',
                      abspath(join(abspath(dirname(abspath(dirname(__file__)))), 'data', 'embeddings.json')))

print(INDEX_FILENAME)

app = Flask(__name__)


with open(PATHS_JSON, 'r') as fp:
    PATHS = json.load(fp)

with open(EMBEDDING_JSON, 'r') as fp:
    embeddings = json.load(fp)

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

nodes = [PyNode(path, vector) for path, vector in zip(PATHS, embeddings)]
nsw = PyNSW('l2')
for node in nodes:
    nsw.nn_insert(node, 1, 1000)

def get_closest_celeb_filename_annoy(vector):
    closest_celeb_index = embedding_index.get_nns_by_vector(vector, 1)[0]
    return str(PATHS[closest_celeb_index])


def get_closest_celeb_filename_nsw(vector):
    return nsw.nn_search(PyNode('1', vector), 1, 1)[0][1]

@app.route('/', methods=['POST'])
def get_closest_vector():
    content = request.get_json(silent=True)
    vector = content['vector']
    
    closest_celeb_filename = get_closest_celeb_filename_annoy(vector)
    response = {'closest_celeb_filename': closest_celeb_filename}
    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")





