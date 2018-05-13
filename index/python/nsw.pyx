from python.node cimport PyNode
from python.dist cimport Distance, Distance_l1, Distance_l2


cdef class PyNSW:
    def __cinit__(self, const string& dist_type):
        self.dist_type = dist_type
        if dist_type == 'l1' or dist_type == 'l2':
            self.nsw = new NSW(dist_type)
        else:
            raise TypeError('Unknown distance type: {}'.format(dist_type))

    def __dealloc__(self):
        del self.nsw

    @property
    def dist_type(self):
        return self.dist_type

    @dist_type.setter
    def dist_type(self, value):
        raise TypeError('You cannot change distance type')

    def nn_insert(self, PyNode node, size_t num_iters, size_t num_neighbors):
        self.nsw.NNInsert(node.node, num_iters, num_neighbors)

    def nn_search(self, PyNode node, size_t num_iters, size_t num_neighbors):
        dists, indices = zip(*self.nsw.NNSearch(node.node, num_iters, num_neighbors))
        file_paths = [self.nsw.getNode(idx).get_path() for idx in indices]
        return zip(dists, file_paths)
