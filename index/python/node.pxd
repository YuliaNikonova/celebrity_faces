from libcpp.string cimport string
from libcpp.vector cimport vector


cdef extern from "node.h" namespace "nsw":
    cdef cppclass Node:
        Node()
        const string& getPath()
        const vector[float]& getCoord()
        void setPath(const string& new_file_path)
        void setCoord(const vector[float]& new_coord)
        string& getPathRef()
        vector[float]& getCoordRef()
        string file_path
        vector[float] coord

cdef class PyNode:
    cdef Node* node
