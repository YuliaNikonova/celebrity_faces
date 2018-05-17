import json
import jsonpickle
import os

from flask import Flask, request, Response
from python.index import create_node, PyNSW

INDEX_FILENAME = os.getenv(
    'INDEX_FILENAME',
    os.path.abspath(os.path.join(__file__, '..', '..', 'data', 'index.ann')))
PATHS_JSON = os.getenv(
    'PATHS_JSON',
    os.path.abspath(os.path.join(__file__, '..', '..', 'data', 'paths.json')))
EMBEDDING_JSON = os.getenv(
    'EMBEDDING_JSON',
    os.path.abspath(os.path.join(__file__, '..', '..', 'data', 'embeddings.json')))


def create_index(index_path):
    index = PyNSW('l2')
    if os.path.exists(index_path):
        index.load(index_path)
    else:
        with open(PATHS_JSON, 'r') as fp:
            print('Loading paths')
            paths = json.load(fp)
        with open(EMBEDDING_JSON, 'r') as fp:
            print('Loading embeddings')
            embeddings = json.load(fp)
        print('Creating nodes')
        nodes = [create_node(path, vector) for path, vector in zip(paths, embeddings)]
        print('Inserting nodes')
        for idx, node in enumerate(nodes):
            if idx % 500 == 0:
                print('{} nodes inserted'.format(idx))
            index.nn_insert(node, 3, 1000)
        index.save(index_path)


if __name__ == '__main__':
    index = create_index(INDEX_FILENAME)
    app = Flask(__name__)

    @app.route('/', methods=['POST'])
    def get_closest_vector():
        content = request.get_json(silent=True)
        vector = content['vector']

        closest_celeb_filename = index.nn_search(create_node('1', vector), 1, 1)[0][1]
        response = {'closest_celeb_filename': closest_celeb_filename}
        response_pickled = jsonpickle.encode(response)
        return Response(response=response_pickled, status=200, mimetype="application/json")

    app.run(host='0.0.0.0', port=5002, debug=False)
