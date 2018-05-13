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

from python.index import PyNode, PyDistance_l1, PyDistance_l2, PyNSW
from tqdm import tqdm, trange


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
            nsw.nn_insert(PyNode(str(i), v), 1, 1000)

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

    #def test_glove_25(self):
    #    self._test_index('glove-25-angular', 69.00)

    #def test_nytimes_16(self):
    #    self._test_index('nytimes-16-angular', 80.00)

    def test_fashion_mnist(self):
        self._test_index('fashion-mnist-784-euclidean', 90.00)

if __name__ == "__main__":
    unittest.main()

