from libcpp.string cimport string
from libcpp.vector cimport vector


cdef class PyNode:
    cdef Node c_node
    def __cinit__(self, const string& file_path, const vector[float]& coord):
        self.c_node = Node(file_path, coord)
    def get_coord(self):
        return self.c_node.get_coord()
    def get_path(self):
        return self.c_node.get_path()
