from libcpp.memory cimport shared_ptr
from libcpp.string cimport string
from libcpp.vector cimport vector


cdef extern from "node.h" namespace "nsw":
    cdef cppclass Node:
        Node()
        Node(const Node& newNode)
        const string& getPath()
        const vector[float]& getCoord()
        void setPath(const string& newFilePath)
        void setCoord(const vector[float]& newCoord)
        string& getPathRef()
        vector[float]& getCoordRef()
        string file_path
        vector[float] coord
    ctypedef shared_ptr[Node] NodeShPtr
    ctypedef shared_ptr[const Node] NodeShConstPtr

cdef class PyNode:
    cdef NodeShPtr thisptr
