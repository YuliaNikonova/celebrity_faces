#include <node.h>

namespace nsw {

Node::Node() { }

Node::Node(const std::string& FilePath, const std::vector<float>& Coord)
    : filePath(FilePath)
    , coord(Coord)
{ }

const std::vector<float>& Node::get_coord() const {
    return coord;
}

const std::string& Node::get_path() const {
    return filePath;
}

}