import unittest

import numpy as np
from python.index import PyNSW


class PyNSWTests(unittest.TestCase):

    def test_search(self):
        nsw = PyNSW('l1')


if __name__ == "__main__":
    unittest.main()
