from libcpp.string cimport string
from libcpp.vector cimport vector
from libcpp.utility cimport pair
from python.dist cimport Distance
from python.node cimport Node, NodeShPtr


cdef extern from "nsw.h" namespace "nsw":
    ctypedef pair[float, size_t] NodeData

    cdef cppclass NSW:
        NSW(const string& distType)
        void NNInsert(NodeShPtr node, size_t numIters, size_t numNeighbors, unsigned int randomSeed)
        vector[NodeData] NNSearch(NodeShPtr node, size_t numIters, size_t numNeighbors, unsigned int randomSeed)
        NodeShPtr getNode(size_t idx)
        void save(const string& filePath)
        void load(const string& filePath)
        Distance dist
        string distType
        vector[NodeShPtr] nodes
        vector[vector[size_t]] nodeNeighbors


cdef class PyNSW:
    cdef NSW* thisptr
    cdef string dist_type
