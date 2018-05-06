from python.node cimport PyNode


cdef class PyDistance_l1:
    def __cinit__(self):
        self.dist = Distance_l1()
    def __call__(self, PyNode node1, PyNode node2):
        return self.dist(node1.node, node2.node)


cdef class PyDistance_l2:
    def __cinit__(self):
        self.dist = Distance_l2()
    def __call__(self, PyNode node1, PyNode node2):
        return self.dist(node1.node, node2.node)
