#pragma once

#include <node.h>
#include <vector>

namespace nsw {

template<typename Dist>
class NSW {
public:
    NSW();
    void NNInsert (
        const Node& node,
        std::size_t num_iters,
        std::size_t num_neighbors
    );
    std::vector<std::size_t> NNSearch (
        const Node& node,
        std::size_t num_iters,
        std::size_t num_neighbors
    ) const;
private:
    Dist dist;
    std::vector<const Node*> nodes;
    std::vector<std::vector<size_t>> node_neighbors;
};

}