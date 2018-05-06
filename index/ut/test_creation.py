import unittest

import numpy as np
from python.index import PyNode, PyDistance_l1, PyDistance_l2, PyNSW


class PyNodeTests(unittest.TestCase):

    def test_init_list(self):
        node = PyNode('kek', [1, 2, 3])
        self.assertEqual([1., 2., 3.], node.coord)
        self.assertEqual('kek', node.file_path)

    def test_init_numpy(self):
        node = PyNode('kek', np.array([1, 2, 3]))
        self.assertEqual([1., 2., 3.], node.coord)
        self.assertEqual('kek', node.file_path)

    def test_set_new_values(self):
        node = PyNode('kek', [1, 2, 3])
        new_file_path = 'lol'

        node.file_path = new_file_path
        self.assertEqual(new_file_path, node.file_path)


class PyDistanceTests(unittest.TestCase):
    node1 = PyNode('kek', [1, 2, 3])
    node2 = PyNode('lol', [1, 2, 5])

    def test_l1(self):
        self.assertEqual(2, PyDistance_l1()(self.node1, self.node2))

    def test_l2(self):
        self.assertEqual(2, PyDistance_l2()(self.node1, self.node2))


class PyNSWTests(unittest.TestCase):

    def test_l1(self):
        nsw = PyNSW('l1')
        self.assertEqual('l1', nsw.dist_type)

    def test_l2(self):
        nsw = PyNSW('l2')
        self.assertEqual('l2', nsw.dist_type)

    def test_fail(self):
        fake_dist_type = 'l3'
        with self.assertRaises(TypeError) as context:
            PyNSW(fake_dist_type)
        self.assertEqual('Unknown distance type: {}'.format(fake_dist_type), context.exception.message)


if __name__ == "__main__":
    unittest.main()
