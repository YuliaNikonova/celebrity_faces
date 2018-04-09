import unittest

import numpy as np
from nsw import PyNode


class PyNodeTests(unittest.TestCase):

    def test_init_list(self):
        node = PyNode('kek', [1, 2, 3])
        self.assertEqual(node.get_coord(), [1., 2., 3.])
        self.assertEqual(node.get_path(), 'kek')

    def test_init_numpy(self):
        node = PyNode('kek', np.array([1, 2, 3]))
        self.assertEqual(node.get_coord(), [1., 2., 3.])
        self.assertEqual(node.get_path(), 'kek')


if __name__ == "__main__":
    unittest.main()
