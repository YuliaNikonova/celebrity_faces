from libcpp.string cimport string
from libcpp.vector cimport vector
from libcpp.utility cimport pair
from python.dist cimport Distance
from python.node cimport Node


cdef extern from "nsw.h" namespace "nsw":
    cdef cppclass NSW:
        NSW(const string& dist_type)
        void NNInsert(const Node* node, size_t numIters, size_t numNeighbors)
        vector[pair[float, size_t]] NNSearch(const Node* node, size_t numIters, size_t numNeighbors)
        Node* getNode(size_t idx)
        Distance dist
        string distType
        vector[const Node*] nodes
        vector[vector[size_t]] nodeNeighbors


cdef class PyNSW:
    cdef NSW* nsw
    cdef string dist_type
