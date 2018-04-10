cdef class PyNode:
    def __cinit__(self, const string& file_path, const vector[float]& coord):
        self.node = Node(file_path, coord)
    def get_coord(self):
        return self.node.get_coord()
    def get_path(self):
        return self.node.get_path()
