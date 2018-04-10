#pragma once

#include <string>
#include <vector>

namespace nsw {

class Node {
public:
    Node();
    Node(const std::string& filePath, const std::vector<float>& coord);
    const std::vector<float>& get_coord() const;
    const std::string& get_path() const;
private:
    std::string FilePath;
    std::vector<float> Coord;
};

}