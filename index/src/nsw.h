#pragma once

#include <dist.h>
#include <node.h>

#include <string>
#include <vector>
#include <utility>

namespace nsw {

using nodeData = std::pair<float, std::size_t>;

class NSW {
public:
    NSW(const std::string& DistType);
    ~NSW();
    void NNInsert (
        const Node* node,
        std::size_t numIters,
        std::size_t numNeighbors
    );
    std::vector<nodeData> NNSearch (
        const Node* node,
        std::size_t numIters,
        std::size_t numNeighbors
    ) const;
    const Node* getNode (std::size_t idx) const;
    void save(const std::string& filePath);
    void load(const std::string& filePath);
private:
    Distance* dist;
    std::string distType;
    std::vector<const Node*> nodes;
    std::vector<std::vector<size_t>> nodeNeighbors;
};

}