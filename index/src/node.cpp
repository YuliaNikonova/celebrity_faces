#include <node.h>

namespace nsw {

Node::Node() { }

Node::Node(const std::string& FilePath, const std::vector<float>& Coord)
    : filePath(FilePath)
    , coord(Coord)
{ }

const std::string& Node::getPath() const {
    return filePath;
}

const std::vector<float>& Node::getCoord() const {
    return coord;
}

void Node::setPath(const std::string& newFilePath) {
    filePath = newFilePath;
}

void Node::setCoord(const std::vector<float>& newCoord) {
    coord = newCoord;
}

std::string& Node::getPathRef() {
    return filePath;
}

std::vector<float>& Node::getCoordRef() {
    return coord;
}

}