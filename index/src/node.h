#pragma once

#include <memory>
#include <string>
#include <vector>

namespace nsw {

class Node {
public:
    Node() {};
    Node(const Node& newNode);
    Node(const std::string& FilePath, const std::vector<float>& Coord);
    ~Node() {};
    const std::string& getPath() const;
    const std::vector<float>& getCoord() const;
    void setPath(const std::string& newFilePath);
    void setCoord(const std::vector<float>& newCoord);
    std::string& getPathRef();
    std::vector<float>& getCoordRef();
private:
    std::string filePath;
    std::vector<float> coord;
};

typedef std::shared_ptr<Node> NodeShPtr;
typedef std::shared_ptr<const Node> NodeShConstPtr;

}