#include <node.h>

namespace nsw {

Node::Node() { }

Node::Node(const std::string& FilePath, const std::vector<float>& Coord)
    : filePath(FilePath)
    , coord(Coord)
{ }

const std::string& Node::get_path() const {
    return filePath;
}

const std::vector<float>& Node::get_coord() const {
    return coord;
}

void Node::set_path(const std::string& newFilePath) {
    filePath = newFilePath;
}

void Node::set_coord(const std::vector<float>& newCoord) {
    coord = newCoord;
}

}