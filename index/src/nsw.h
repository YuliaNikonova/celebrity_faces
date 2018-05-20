#pragma once

#include <dist.h>
#include <node.h>

#include <memory>
#include <string>
#include <vector>
#include <utility>

namespace nsw {

typedef std::pair<float, std::size_t> NodeData;
typedef std::shared_ptr<NodeData> NodeDataShPtr;

class NSW {
public:
    NSW(const std::string& DistType);
    ~NSW();
    void NNInsert (
        NodeShPtr node,
        std::size_t numIters,
        std::size_t numNeighbors
    );
    std::vector<NodeData> NNSearch (
        NodeShPtr node,
        std::size_t numIters,
        std::size_t numNeighbors
    ) const;
    NodeShPtr getNode (std::size_t idx) const;
    void save(const std::string& filePath);
    void load(const std::string& filePath);
private:
    Distance* dist;
    std::string distType;
    std::vector<NodeShPtr> nodes;
    std::vector<std::vector<size_t>> nodeNeighbors;
};

}