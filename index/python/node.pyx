from cython.operator cimport dereference as deref


cdef class PyNode:
    def __cinit__(self, PyNode node=None):
        if node is None:
            self.thisptr = NodeShPtr(new Node())
        else:
            self.thisptr = NodeShPtr(new Node(deref(node.thisptr)))

    def __dealloc__(self):
        if self.thisptr.get() is not NULL:
            self.thisptr.reset()

    @property
    def coord(self):
        return deref(self.thisptr).getCoord()

    @coord.setter
    def coord(self, const vector[float]& new_coord):
        deref(self.thisptr).setCoord(new_coord)

    @property
    def file_path(self):
        return deref(self.thisptr).getPath()

    @file_path.setter
    def file_path(self, const string& new_file_path):
        deref(self.thisptr).setPath(new_file_path)


def create_node(const string& file_path, const vector[float]& coord):
    cdef PyNode node = PyNode()
    node.file_path = file_path
    node.coord = coord
    return node
