#pragma once

#include <string>
#include <vector>

namespace nsw {

class Node {
public:
    Node();
    Node(const std::string& FilePath, const std::vector<float>& Coord);
    const std::string& get_path() const;
    const std::vector<float>& get_coord() const;
    void set_path(const std::string& newFilePath);
    void set_coord(const std::vector<float>& newCoord);
private:
    std::string filePath;
    std::vector<float> coord;
};

}