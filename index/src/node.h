#pragma once

#include <string>
#include <vector>

namespace nsw {

class Node {
public:
    Node();
    Node(const std::string& FilePath, const std::vector<float>& Coord);
    const std::vector<float>& get_coord() const;
    const std::string& get_path() const;
private:
    std::string filePath;
    std::vector<float> coord;
};

}