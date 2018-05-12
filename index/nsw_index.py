import numpy as np
from python.index import PyNode, PyDistance_l1, PyDistance_l2, PyNSW
from os.path import dirname, join, abspath
from os import getenv
import json
import jsonpickle




PATHS_JSON = getenv('PATHS_JSON',
                    abspath(join(abspath(dirname(abspath(dirname(__file__)))), 'data', 'paths.json')))
EMBEDDING_JSON = getenv('EMBEDDING_JSON',
                        abspath(join(abspath(dirname(abspath(dirname(__file__)))), 'data', 'embeddings.json')))

with open(PATHS_JSON, 'r') as fp:
    PATHS = json.load(fp)

with open(EMBEDDING_JSON, 'r') as fp:
    EMBEDDINGS = json.load(fp)

nodes = [PyNode(path, vector) for path, vector in zip(PATHS, EMBEDDINGS)]


nsw = PyNSW('l2')
for node in nodes:
    nsw.nn_insert(node, 1, 10)

random_vector = EMBEDDINGS[100]
print(PATHS[100])
print(random_vector)

neighbors = nsw.nn_search(PyNode('1', random_vector), 5, 3)

print(neighbors)
