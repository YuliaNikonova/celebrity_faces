import errno
import os
import time
from cython.operator cimport dereference as deref
from python.node cimport PyNode
from python.dist cimport Distance, Distance_l1, Distance_l2


cdef class PyNSW:
    def __cinit__(self, const string& dist_type):
        self.dist_type = dist_type
        if dist_type == 'l1' or dist_type == 'l2':
            self.thisptr = new NSW(dist_type)
        else:
            raise TypeError('Unknown distance type: {}'.format(dist_type))

    def __dealloc__(self):
        if self.thisptr is not NULL:
            del self.thisptr

    @property
    def dist_type(self):
        return self.dist_type

    @dist_type.setter
    def dist_type(self, value):
        raise TypeError('You cannot change distance type')

    def nn_insert(self, PyNode node, size_t num_iters, size_t num_neighbors, unsigned int random_seed=0):
        deref(self.thisptr).NNInsert(node.thisptr, num_iters, num_neighbors, random_seed)

    def nn_search(self, PyNode node, size_t num_iters, size_t num_neighbors, unsigned int random_seed=0):
        if random_seed == 0:
            random_seed = time.time()
        search_results = deref(self.thisptr).NNSearch(node.thisptr, num_iters, num_neighbors, random_seed)
        dists, indices = zip(*search_results)
        file_paths = [deref(deref(self.thisptr).getNode(idx)).getPath() for idx in indices]
        return zip(dists, file_paths)

    def save(self, file_path):
        try:
            os.makedirs(file_path)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
        deref(self.thisptr).save(file_path)

    def load(self, file_path):
        if not os.path.exists(file_path):
            raise ValueError('Provided index path does not exist: {}'.format(file_path))
        deref(self.thisptr).load(file_path)
