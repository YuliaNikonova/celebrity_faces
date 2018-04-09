from libcpp.string cimport string
from libcpp.vector cimport vector


cdef extern from "node.h" namespace "nsw":
    cdef cppclass Node:
        Node()
        Node(const string& file_path, const vector[float]& coord) except +
        const vector[float]& get_coord()
        const string& get_path()
        string file_path
        vector[float] coord
