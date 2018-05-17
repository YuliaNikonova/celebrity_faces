#pragma once

#include <string>
#include <vector>

namespace nsw {

class Node {
public:
    Node();
    Node(const std::string& FilePath, const std::vector<float>& Coord);
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

}