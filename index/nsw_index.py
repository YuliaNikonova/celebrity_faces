import json
from os import getenv
from os.path import abspath, join

from python.index import create_node, PyNSW

PATHS_JSON = getenv(
    'PATHS_JSON',
    abspath(join(__file__, '..', '..', 'data', 'paths.json')))
EMBEDDING_JSON = getenv(
    'EMBEDDING_JSON',
    abspath(join(__file__, '..', '..', 'data', 'embeddings.json')))


if __name__ == '__main__':
    with open(PATHS_JSON) as fp:
        paths = json.load(fp)
    with open(EMBEDDING_JSON) as fp:
        embeddings = json.load(fp)

    nodes = [create_node(path, vector) for path, vector in zip(paths, embeddings)]

    nsw = PyNSW('l2')
    for node in nodes:
        nsw.nn_insert(node, 1, 100)

    random_vector = embeddings[100]
    print(paths[100])
    print(random_vector)

    neighbors = nsw.nn_search(create_node('kek', random_vector), 5, 3)
    print(neighbors)
