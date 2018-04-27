#include <nsw.h>
#include <algorithm>
#include <numeric>
#include <queue>
#include <stdexcept>

namespace nsw {

NSW::NSW(const std::string& DistType)
    : distType(DistType)
    , nodes(0)
    , nodeNeighbors(0) {
        if (distType == "l1") {
            dist = new Distance_l1();
        } else if (distType == "l2") {
            dist = new Distance_l2();
        } else {
            throw std::invalid_argument("Unknown distance type");
        }
};

NSW::~NSW() {
    delete dist;
}

void NSW::NNInsert (
    const Node& node,
    std::size_t numIters,
    std::size_t numNeighbors
) {
    auto neighbors = NNSearch(node, numIters, numNeighbors);
    std::size_t nodeIdx = nodes.size();
    nodes.push_back(&node);
    for (auto curPair : neighbors) {
        nodeNeighbors[curPair.second].push_back(nodeIdx);
        nodeNeighbors[nodeIdx].push_back(curPair.second);
    }
};


std::vector<nodeData> NSW::NNSearch (
    const Node& node,
    std::size_t numIters,
    std::size_t numNeighbors
) const {
    std::size_t N = nodes.size();
    std::vector<bool> visited(N, false);
    // increasing order
    std::priority_queue<nodeData> result;
    // decreasing order
    std::priority_queue<nodeData, std::vector<nodeData>, std::greater<nodeData>> candidates;

    // preallocate random indices for fast random search
    std::vector<std::size_t> randomIndices(N);
    std::iota(randomIndices.begin(), randomIndices.end(), 0);
    std::random_shuffle(randomIndices.begin(), randomIndices.end());
    std::size_t randomIdx = 0;

    for (std::size_t iter = 0; iter < numIters; ++iter) {
        // put random node in candidates
        for (; (randomIdx < N) && !(visited[randomIndices[randomIdx]]); ++randomIdx) {}
        if (randomIdx == N) { break; }

        auto candidateIdx = randomIndices[randomIdx];
        visited[candidateIdx] = true;
        candidates.push(std::make_pair(dist->operator()(node, *nodes[candidateIdx]), candidateIdx));

        std::vector<nodeData> tmpResult;

        while (true) {
            // get closest node from candidates
            auto curPair = candidates.top();
            candidates.pop();
            // check stop condition
            if (curPair.first > result.top().first) { break; }

            for (auto neighborIdx : nodeNeighbors[candidateIdx]) {
                if (!visited[neighborIdx]) {
                    visited[neighborIdx] = true;
                    tmpResult.push_back(std::make_pair(dist->operator()(node, *nodes[neighborIdx]), neighborIdx));
                    candidates.push(tmpResult.back());
                }
            }

            if (candidates.empty()) { break; }
        }

        // add nodes from tmpResult to result maintaining its size
        for (auto curPair : tmpResult) {
            result.push(curPair);
            if (result.size() > numNeighbors) {
                result.pop();
            }
        }
    }

    // convert result to vector
    std::vector<nodeData> neighbors(numNeighbors);
    for (std::size_t idx = 0; idx < numNeighbors; ++idx) {
        neighbors[idx] = result.top();
        result.pop();
    }
    return neighbors;
};

}
