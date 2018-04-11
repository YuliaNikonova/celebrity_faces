#include <nsw.h>
#include <algorithm>
#include <numeric>
#include <queue>
#include <utility>

namespace nsw {

template<typename Dist>
NSW<Dist>::NSW()
    : nodes(0)
    , node_neighbors(0) {
    dist = Dist();
};

template<typename Dist>
void NSW<Dist>::NNInsert (
    const Node& node,
    std::size_t num_iters,
    std::size_t num_neighbors
) {
    auto neighbors = NNSearch(node, num_iters, num_neighbors);
    auto node_idx = nodes.size();
    nodes.push_back(&node);
    for (auto idx : neighbors) {
        node_neighbors[idx].push_back(node_idx);
        node_neighbors[node_idx].push_back(idx);
    }
};

template<typename Dist>
std::vector<std::size_t> NSW<Dist>::NNSearch (
    const Node& node,
    std::size_t num_iters,
    std::size_t num_neighbors
) const {
    std::size_t N = nodes.size();
    std::priority_queue<std::pair<float, std::size_t>> result;
    std::priority_queue<std::pair<float, std::size_t>> candidates;
    std::vector<bool> visited(N, false);

    std::vector<std::size_t> random_indices(N);
    std::iota(random_indices.begin(), random_indices.end(), 0);
    std::random_shuffle(random_indices.begin(), random_indices.end());
    std::size_t random_idx = 0;

    for (std::size_t i = 0; i < num_iters; ++i) {
        for (; (random_idx < N) && !(visited[random_indices[random_idx]]); ++random_idx) {}
        if (random_idx == N) { break; }

        auto candidate_idx = random_indices[random_idx];
        visited[candidate_idx] = true;
        candidates.push(std::make_pair(dist(node, *nodes[candidate_idx]), candidate_idx));

        while (true) {
            auto cur_pair = candidates.top();
            candidates.pop();
            if (cur_pair.first > result.top().first) { break; }

            for (auto neighbor_idx : node_neighbors[candidate_idx]) {
                if (!visited[neighbor_idx]) {
                    visited[neighbor_idx] = true;
                    candidates.push(std::make_pair(dist(node, *nodes[neighbor_idx]), neighbor_idx));
                }
            }
        }
    }

    std::vector<std::size_t> neighbors(num_neighbors, 0);
    return neighbors;
};

}
