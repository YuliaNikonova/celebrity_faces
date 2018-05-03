cdef class PyNode:
    def __cinit__(self, const string& file_path, const vector[float]& coord):
        self.node = Node(file_path, coord)

    @property
    def coord(self):
        return self.node.get_coord()

    @property
    def file_path(self):
        return self.node.get_path()

    @file_path.setter
    def file_path(self, new_file_path):
        self.node.set_path(new_file_path)
