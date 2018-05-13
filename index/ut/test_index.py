import unittest
from operator import itemgetter

import numpy as np

from python.index import create_node, PyNSW

NUM_NODES = 10


class PyNSWTests(unittest.TestCase):
    nodes = [create_node(str(i), [i**2]) for i in range(NUM_NODES)]

    def _create_index(self, num_neighbors=(NUM_NODES - 1), num_iters=1):
        nsw = PyNSW('l2')
        # connect each node to `num_neighbors` other nodes
        for node in self.nodes:
            nsw.nn_insert(node, num_iters, num_neighbors)
        return nsw

    def test_search_full(self):
        nsw = self._create_index()
        # check that the node is closest to itself
        for node in self.nodes:
            neighbors = nsw.nn_search(node, 1, 1)
            self.assertEqual(node.file_path, neighbors[0][1])

    def test_search_half(self):
        nsw = self._create_index(num_neighbors=(NUM_NODES / 2))

        # count top3 accuracy depending on number of iterations
        NUM_ITERS = 3
        count = np.zeros(NUM_ITERS)

        for num_iter in range(1, NUM_ITERS + 1):
            accuracy = 0.0
            for node in self.nodes:
                neighbors = nsw.nn_search(node, num_iter, 3)
                accuracy += (node.file_path in map(itemgetter(1), neighbors))
            count[num_iter - 1] = accuracy / NUM_NODES

        self.assertTrue(np.all(count >= 0.8))

    def test_search_quarter(self):
        nsw = self._create_index(num_neighbors=(NUM_NODES / 4))

        # count top3 accuracy depending on number of iterations
        NUM_ITERS = 3
        count = np.zeros(NUM_ITERS)

        for num_iter in range(1, NUM_ITERS + 1):
            accuracy = 0.0
            for node in self.nodes:
                neighbors = nsw.nn_search(node, num_iter, 3)
                accuracy += (node.file_path in map(itemgetter(1), neighbors))
            count[num_iter - 1] = accuracy / NUM_NODES

        self.assertTrue(np.all(count >= np.array([0.5, 0.7, 0.9])))

if __name__ == "__main__":
    unittest.main()
