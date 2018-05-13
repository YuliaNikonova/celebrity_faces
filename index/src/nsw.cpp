#include <nsw.h>
#include <algorithm>
#include <numeric>
#include <queue>
#include <stdexcept>

#include <iostream>
#include <iomanip>

namespace nsw {

static constexpr double EPSILON = 1e-9;
static constexpr bool DEBUG = false;

std::ostream& operator<<(std::ostream& os, const Node& node) {
    os << '(' << node.get_path() << ';' << std::setprecision(2);
    for (auto num : node.get_coord()) {
        os << num << ',';
    }
    return os << ')';
};

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
};

void NSW::NNInsert (
    const Node* node,
    std::size_t numIters,
    std::size_t numNeighbors
) {
    // std::cout << "Init: " << node << std::endl;
    auto neighbors = NNSearch(node, numIters, numNeighbors);
    std::size_t nodeIdx = nodes.size();

    nodes.push_back(node);
    nodeNeighbors.push_back({});

    if (neighbors.empty()) {
        // Connect to all previous nodes
        for (std::size_t idx = 0; idx < nodeIdx; ++idx) {
            nodeNeighbors.at(nodeIdx).push_back(idx);
            nodeNeighbors.at(idx).push_back(nodeIdx);
        }
    } else {
        for (auto curPair : neighbors) {
            // std::cout << curPair.first << ' ' << *nodes[curPair.second] << std::endl;
            nodeNeighbors.at(nodeIdx).push_back(curPair.second);
            nodeNeighbors.at(curPair.second).push_back(nodeIdx);
        }
    }
    // std::cout << std::endl;
};

std::vector<nodeData> NSW::NNSearch (
    const Node* node,
    std::size_t numIters,
    std::size_t numNeighbors
) const {
    if (DEBUG) { std::cout << "\tSearch: " << *node << std::endl; }
    std::size_t N = nodes.size();

    // check if index is empty
    if (N == 0) {
        return std::vector<nodeData>();
    }

    std::vector<bool> visited(N, false);
    // decreasing order; size is always <= numNeighbors
    std::priority_queue<nodeData> result;
    // increasing order
    std::priority_queue<nodeData, std::vector<nodeData>, std::greater<nodeData>> candidates;

    // preallocate random indices for fast random search
    std::vector<std::size_t> randomIndices(N);
    std::iota(randomIndices.begin(), randomIndices.end(), 0);
    std::random_shuffle(randomIndices.begin(), randomIndices.end());
    // lookup table for positioning index in randomIndices
    std::vector<std::size_t> randomIndicesLookup(N);
    for (std::size_t idx = 0; idx < N; ++idx) {
        randomIndicesLookup[randomIndices[idx]] = idx;
    }
    // track the first unvisited index in randomIndices
    std::size_t unvisitedIdx = 0;

    for (std::size_t iter = 0; iter < numIters; ++iter) {
        if (DEBUG) { std::cout << "unvisitedIdx: " << unvisitedIdx << std::endl; }
        if (unvisitedIdx >= N) {
            // exhausted candidates
            break;
        }

        // put random node in candidates
        auto candidateIdx = randomIndices[unvisitedIdx];
        std::vector<nodeData> tmpResult = {std::make_pair(dist->operator()(node, nodes[candidateIdx]), candidateIdx)};
        candidates.push(tmpResult.back());
        // update visited nodes
        visited[candidateIdx] = true;
        std::swap(randomIndices[randomIndicesLookup[candidateIdx]], randomIndices[unvisitedIdx]);
        ++unvisitedIdx;

        while (true) {
            // get closest node from candidates
            auto curPair = candidates.top();
            candidates.pop();
            // check stop condition
            // if (!result.empty()) { std::cout << result.top().second << ' ' << curPair.second << std::endl; }
            if (!result.empty() && (curPair.first - result.top().first >= EPSILON) && (tmpResult.size() < numNeighbors)) { break; }

            for (auto neighborIdx : nodeNeighbors[candidateIdx]) {
                if (!visited[neighborIdx]) {
                    tmpResult.push_back(std::make_pair(dist->operator()(node, nodes[neighborIdx]), neighborIdx));
                    candidates.push(tmpResult.back());
                    // update visited nodes
                    visited[neighborIdx] = true;
                    std::swap(randomIndices[randomIndicesLookup[neighborIdx]], randomIndices[unvisitedIdx]);
                    ++unvisitedIdx;
                }
            }

            if (candidates.empty()) { break; }
        }

        // add nodes from tmpResult to result maintaining its size
        for (auto curPair : tmpResult) {
            if (DEBUG) { std::cout << "push: " << curPair.first << ' ' << *nodes[curPair.second] << std::endl; }
            result.push(curPair);
            if (result.size() > numNeighbors) {
                if (DEBUG) { std::cout << "pop: " << *nodes[result.top().second] << std::endl; }
                result.pop();
            }
        }
    }

    // convert result to vector
    auto numResults = result.size();
    std::vector<nodeData> neighbors(numResults);
    for (std::size_t idx = 0; idx < numResults; ++idx) {
        neighbors[numResults - 1 - idx] = result.top();
        result.pop();
    }
    return neighbors;
};

const Node* NSW::getNode(std::size_t idx) const{
    return nodes.at(idx);
};

}
