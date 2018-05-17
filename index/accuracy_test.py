# Copyright (c) 2013 Spotify AB
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.

from __future__ import print_function

import h5py
import unittest
import os
from os.path import dirname, join, abspath, exists
from annoy import AnnoyIndex
try:
    from urllib import urlretrieve
except ImportError:
    from urllib.request import urlretrieve # Python 3
import gzip
from nose.plugins.attrib import attr

import numpy as np

from python.index import PyNode, PyDistance_l1, PyDistance_l2, PyNSW, create_node
from tqdm import tqdm, trange
import json


class AccuracyTest(unittest.TestCase):
    def _get_index(self, dataset):
        vectors_fn = join(os.getenv('ACCURACY_TEST_DATA_PATH',
               abspath(join(abspath(dirname(abspath(dirname(__file__)))), 'data', 'test'))), dataset + '.hdf5')

        if not exists(vectors_fn):
            url = 'http://vectors.erikbern.com/%s.hdf5' % dataset
            print('downloading', url, '->', vectors_fn)
            urlretrieve(url, vectors_fn)

        index_fn = os.path.join(dataset + '.annoy')
        dataset_f = h5py.File(vectors_fn)
        distance = dataset_f.attrs['distance']
        f = dataset_f['train'].shape[1]
        annoy = AnnoyIndex(f, distance)

        print('building nsw index')
        nsw = PyNSW('l2')
        for i in trange(dataset_f['train'].shape[0]):
            v = dataset_f['train'][i]
            nsw.nn_insert(PyNode(str(i), v), 1, 100)

        if not os.path.exists(index_fn):
            print('adding items', distance, f)
            for i, v in enumerate(dataset_f['train']):
                annoy.add_item(i, v)

            print('building annoy index')
            annoy.build(10)
            annoy.save(index_fn)
        else:
            annoy.load(index_fn)
        return annoy, dataset_f

    def _test_index(self, dataset, exp_accuracy):
        annoy, dataset_f = self._get_index(dataset)

        n, k_annoy, k_nsw = 0, 0, 0

        for i, v in enumerate(dataset_f['test']):
            js_fast = annoy.get_nns_by_vector(v, 10, 1000)
            js_real = dataset_f['neighbors'][i][:10]
            js_fast_nsw = [int(result[1]) for result in nsw.nn_search(PyNode('1', v), 1, 10)]

            assert len(js_fast) == 10
            assert len(js_real) == 10
            assert len(js_fast_nsw) == 10

            n += 10
            k_annoy += len(set(js_fast).intersection(js_real))
            k_nsw += len(set(js_fast_nsw).intersection(js_real))

        accuracy_annoy = 100.0 * k_annoy / n
        accuracy_nsw = 100.0 * k_nsw / n
        print('Annoy: %50s accuracy: %5.2f%% (expected %5.2f%%)' % (dataset, accuracy_annoy, exp_accuracy))
        print('NSW: %50s accuracy: %5.2f%%' % (dataset, accuracy_nsw))

        self.assertTrue(accuracy > exp_accuracy - 1.0) # should be within 1%

    #def test_fashion_mnist(self):
    #    self._test_index('fashion-mnist-784-euclidean', 90.00)


    def test_celeba_embedding(self):
        PATHS_JSON = os.getenv('PATHS_JSON', abspath(join(__file__, '..', '..', 'data', 'paths_celeba.json')))

        EMBEDDING_JSON = os.getenv('EMBEDDING_JSON', abspath(join(__file__, '..', '..', 'data', 'embeddings_celeba.json')))


        INDEX_FILENAME = os.getenv('INDEX_FILENAME', os.path.abspath(os.path.join(__file__, '..', '..', 'data', 'index_celeba.ann')))

        NSW_INDEX_FILENAME = os.getenv('NSW_INDEX_FILENAME', os.path.abspath(os.path.join(__file__, '..', '..', 'data', 'index_celeba_nsw')))

        TEST_CASES_FILENAME = os.getenv('TEST_CASES_FILENAME',
            os.path.abspath(os.path.join(__file__, '..', '..', 'data', 'index_celeba_test_cases.json')))

        with open(PATHS_JSON, 'r') as fp:
            print('Loading paths')
            paths = np.array(json.load(fp))
        with open(EMBEDDING_JSON, 'r') as fp:
            print('Loading embeddings')
            embeddings = json.load(fp)

        with open(TEST_CASES_FILENAME, 'r') as fp:
            print('Loading test_cases')
            test_cases = json.load(fp)


        annoy = AnnoyIndex(len(embeddings[0]))    
        annoy_index = annoy.load(INDEX_FILENAME)

        print('building nsw index')
        nsw_index = PyNSW('l2')
        print('Creating nodes')
        nodes = [create_node(path, vector) for path, vector in zip(paths, embeddings)]
        print('Inserting nodes')
        for node in tqdm(nodes):
            nsw_index.nn_insert(node, 3, 10)

        n, k_annoy, k_nsw = 0, 0, 0

        print('Calculating accuracy on CelebA')

        for tk in test_cases:
            vector = embeddings[int(tk['embedding_index'])]
            
            closest_paths_real = tk['closest_paths_real']

            closest_paths_annoy = paths[annoy.get_nns_by_vector(vector, 10, 1000)]

            closest_paths_nsw = [n[1] for n in nsw_index.nn_search(create_node('kek', vector), 3, 10)]

            assert len(closest_paths_real) == 10
            assert len(closest_paths_annoy) == 10
            assert len(closest_paths_nsw) == 10

            n += 10
            k_annoy += len(set(closest_paths_annoy).intersection(closest_paths_real))
            k_nsw += len(set(closest_paths_nsw).intersection(closest_paths_real))


        print('Annoy accuracy on CelebA embeddings: {:.3f}%'.format(100.0 * k_annoy / n))
        print('NSW accuracy on CelebA embeddings: {:.3f}%'.format(100.0 * k_nsw / n))






if __name__ == "__main__":
    unittest.main()

