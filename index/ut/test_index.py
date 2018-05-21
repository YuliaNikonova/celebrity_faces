import tempfile
import unittest
from operator import itemgetter

import numpy as np

from python.index import create_node, PyNSW

NUM_NODES = 100


class PyNSWTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.nodes = [create_node(str('node_{}'.format(i)), [i**2]) for i in range(NUM_NODES)]

    @classmethod
    def tearDownClass(cls):
        del cls.nodes

    def _create_index(self, num_neighbors=(NUM_NODES - 1), num_iters=1):
        nsw = PyNSW('l2')
        # connect each node to `num_neighbors` other nodes
        for i, node in enumerate(self.nodes):
            nsw.nn_insert(node, num_iters, num_neighbors, random_seed=1334 + i)
        return nsw

    def test_search_full(self):
        print('test_search_full')
        nsw = self._create_index()
        # check that the node is closest to itself
        for node in self.nodes:
            neighbors = nsw.nn_search(node, 1, 1, random_seed=1334)
            self.assertEqual(node.file_path, neighbors[0][1])

    def test_search_half(self):
        print('test_search_half')
        nsw = self._create_index(num_neighbors=(NUM_NODES / 2))

        # count top3 accuracy depending on number of iterations
        NUM_ITERS = 3
        count = np.zeros(NUM_ITERS)

        for num_iter in range(1, NUM_ITERS + 1):
            accuracy = 0.0
            for node in self.nodes:
                neighbors = nsw.nn_search(node, num_iter, 10, random_seed=1334)
                accuracy += (node.file_path in map(itemgetter(1), neighbors))
            count[num_iter - 1] = accuracy / NUM_NODES
        self.assertTrue(np.all(count == 1.))

    def test_search_quarter(self):
        print('test_search_quarter')
        nsw = self._create_index(num_neighbors=(NUM_NODES / 4))

        # count top3 accuracy depending on number of iterations
        NUM_ITERS = 3
        count = np.zeros(NUM_ITERS)

        for num_iter in range(1, NUM_ITERS + 1):
            accuracy = 0.0
            for node in self.nodes:
                neighbors = nsw.nn_search(node, num_iter, 1, random_seed=1334)
                accuracy += (node.file_path in map(itemgetter(1), neighbors))
            count[num_iter - 1] = accuracy / NUM_NODES
        self.assertTrue(np.all(count == 1.))

    def test_save_load(self):
        print('test_save_load')
        nsw = self._create_index()
        index_path = tempfile.NamedTemporaryFile(delete=False).name
        nsw.save(index_path)

        empty_nsw = PyNSW('l2')
        empty_nsw.load(index_path)

        # compare original and loaded index on different number of iterations
        NUM_ITERS = 1

        for num_iter in range(1, NUM_ITERS + 1):
            for node in self.nodes:
                self.assertEqual(
                    nsw.nn_search(node, num_iter, 3, random_seed=1334),
                    empty_nsw.nn_search(node, num_iter, 3, random_seed=1334)
                )


if __name__ == "__main__":
    unittest.main()
