import unittest

import numpy as np
from python.nsw import PyNode, PyDistance_l1, PyDistance_l2


class PyNodeTests(unittest.TestCase):

    def test_init_list(self):
        node = PyNode('kek', [1, 2, 3])
        self.assertEqual(node.get_coord(), [1., 2., 3.])
        self.assertEqual(node.get_path(), 'kek')

    def test_init_numpy(self):
        node = PyNode('kek', np.array([1, 2, 3]))
        self.assertEqual(node.get_coord(), [1., 2., 3.])
        self.assertEqual(node.get_path(), 'kek')


class PyDistanceTests(unittest.TestCase):
    node1 = PyNode('kek', [1, 2, 3])
    node2 = PyNode('lol', [1, 2, 5])

    def test_l1(self):
        self.assertEqual(PyDistance_l1()(self.node1, self.node2), 2)

    def test_l2(self):
        self.assertEqual(PyDistance_l2()(self.node1, self.node2), 4)


if __name__ == "__main__":
    unittest.main()
