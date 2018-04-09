#include <node.h>

namespace nsw {

Node::Node() { }

Node::Node(const std::string filePath, std::vector<float> coord)
    : FilePath(filePath)
    , Coord(coord)
{ }

const std::vector<float>& Node::get_coord() const {
    return Coord;
}

const std::string& Node::get_path() const {
    return FilePath;
}

}