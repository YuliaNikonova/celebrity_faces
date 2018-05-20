import json
import jsonpickle
import os

from flask import Flask, request, Response
from python.index import create_node, PyNSW
from tqdm import tqdm


NSW_INDEX_FILENAME = os.getenv(
    'NSW_INDEX_FILENAME',
    os.path.abspath(os.path.join(__file__, '..', '..', 'data', 'index_celeba_nsw')))

PATHS_JSON = os.getenv(
    'PATHS_JSON',
    os.path.abspath(os.path.join(__file__, '..', '..', 'data', 'paths_celeba.json')))
EMBEDDING_JSON = os.getenv(
    'EMBEDDING_JSON',
    os.path.abspath(os.path.join(__file__, '..', '..', 'data', 'embeddings_celeba.json')))





index = PyNSW('l2')

with open(PATHS_JSON, 'r') as fp:
    print('Loading paths')
    paths = json.load(fp)
with open(EMBEDDING_JSON, 'r') as fp:
    print('Loading embeddings')
    embeddings = json.load(fp)
print('Creating nodes')
nodes = [create_node(path, vector) for path, vector in zip(paths, embeddings)]
print('Inserting nodes')
for node in tqdm(nodes):
    index.nn_insert(node, 3, 10)
index.save(NSW_INDEX_FILENAME)