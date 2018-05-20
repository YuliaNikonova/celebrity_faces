#include <nsw.h>
#include <algorithm>
#include <ctime>
#include <numeric>
#include <queue>
#include <stdexcept>
#include <unordered_map>

#include <fstream>
#include <iostream>
#include <iomanip>
#include <iterator>
#include <sstream>

namespace nsw {

static constexpr double EPSILON = 1e-9;
static constexpr bool DEBUG = false;

//------------------------------------------------------------
// Utility functions

std::ostream& operator<<(std::ostream& os, const Node& node) {
    os << '(' << node.getPath() << "; [" << std::setprecision(2);
    for (auto num : node.getCoord()) {
        os << num << ',';
    }
    return os << "])";
}

void write_node(std::ofstream& ofs, const Node* node) {
    // write file path
    const auto& filePath = node->getPath();
    std::size_t len = filePath.size();
    ofs.write(reinterpret_cast<char *>(&len), sizeof(len));
    ofs.write(filePath.c_str(), len * sizeof(char));

    // write coordinates
    const auto& coord = node->getCoord();
    std::size_t ndim = coord.size();
    ofs.write(reinterpret_cast<char *>(&ndim), sizeof(ndim));
    ofs.write(const_cast<char *>(reinterpret_cast<const char *>(&coord[0])), ndim * sizeof(float));
}

void read_node(std::ifstream& ifs, Node* node) {
    // read file path
    auto& filePath = node->getPathRef();
    std::size_t len;
    ifs.read(reinterpret_cast<char *>(&len), sizeof(len));
    std::vector<char> buffer(len);
    ifs.read(reinterpret_cast<char *>(&buffer[0]), len * sizeof(char));
    filePath.assign(buffer.begin(), buffer.end());

    // read coordinates
    auto& coord = node->getCoordRef();
    std::size_t ndim;
    ifs.read(reinterpret_cast<char *>(&ndim), sizeof(ndim));
    coord.resize(ndim);
    ifs.read(reinterpret_cast<char *>(&coord[0]), ndim * sizeof(float));
}

//------------------------------------------------------------

NSW::NSW(const std::string& DistType)
    : distType(DistType)
    , nodes(0)
    , nodeNeighbors(0)
{
    if (distType == "l1") {
        dist = new Distance_l1();
    } else if (distType == "l2") {
        dist = new Distance_l2();
    } else {
        throw std::invalid_argument("Unknown distance type");
    }
}

NSW::~NSW() {
    delete dist;
    for (auto nodeShPtr: nodes) {
        nodeShPtr.reset();
    }
}

void NSW::NNInsert (
    NodeShPtr node,
    std::size_t numIters,
    std::size_t numNeighbors,
    unsigned int randomSeed /*= 0*/
) {
    auto neighbors = NNSearch(node, numIters, numNeighbors, randomSeed);
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
            nodeNeighbors.at(nodeIdx).push_back(curPair.second);
            nodeNeighbors.at(curPair.second).push_back(nodeIdx);
        }
    }
}

std::vector<NodeData> NSW::NNSearch (
    const NodeShPtr node,
    std::size_t numIters,
    std::size_t numNeighbors,
    unsigned int randomSeed /*= 0*/
) const {
    if (DEBUG) { std::cout << "Search: " << *node << std::endl; }
    std::size_t N = nodes.size();

    // set random seed
    if (randomSeed == 0) {
        std::srand(std::time(0));
    } else {
        std::srand(randomSeed);
    }

    // check if index is empty
    if (N == 0) {
        return std::vector<NodeData>();
    }

    std::unordered_map<std::size_t, bool> visited;
    for (std::size_t idx = 0; idx < N; ++idx) {
        visited[idx] = false;
    }
    // decreasing order; size is always <= numNeighbors
    std::priority_queue<NodeData> result;
    // increasing order
    std::priority_queue<NodeData, std::vector<NodeData>, std::greater<NodeData>> candidates;

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
        // put random node in candidates
        while ((unvisitedIdx < N) && (visited[randomIndices[unvisitedIdx]])) { ++unvisitedIdx; }
        if (unvisitedIdx >= N) {
            // exhausted candidates
            break;
        }
        auto candidateIdx = randomIndices[unvisitedIdx];
        candidates.emplace(dist->operator()(node.get(), nodes[candidateIdx].get()), candidateIdx);
        std::vector<NodeData> tmpResult;

        while (true) {
            // get closest node from candidates
            auto curPair = candidates.top();
            candidates.pop();
            // check stop condition
            if (!result.empty() && (curPair.first - result.top().first >= EPSILON) && (tmpResult.size() < numNeighbors)) { break; }

            for (auto neighborIdx : nodeNeighbors[curPair.second]) {
                if (!visited[neighborIdx]) {
                    tmpResult.emplace_back(dist->operator()(node.get(), nodes[neighborIdx].get()), neighborIdx);
                    candidates.push(tmpResult.back());
                    visited[neighborIdx] = true;
                }
            }

            if (candidates.empty()) { break; }
        }

        // add nodes from tmpResult to result maintaining its size
        for (auto curPair : tmpResult) {
            if (DEBUG) { std::cout << "\tpush: " << curPair.first << ' ' << *nodes[curPair.second].get() << std::endl; }
            result.push(curPair);
            if (result.size() > numNeighbors) {
                if (DEBUG) { std::cout << "\tpop: " << *nodes[result.top().second].get() << std::endl; }
                result.pop();
            }
        }
    }

    // convert result to vector
    auto numResults = result.size();
    if (DEBUG) { std::cout << "Collecting " << numResults << " results" << std::endl; }
    std::vector<NodeData> neighbors(numResults);
    for (std::size_t idx = 0; idx < numResults; ++idx) {
        neighbors[numResults - 1 - idx] = result.top();
        result.pop();
    }
    return neighbors;
}

NodeShPtr NSW::getNode(std::size_t idx) const{
    return nodes.at(idx);
}

void NSW::save(const std::string& filePath) {
    std::ofstream ofs(filePath, std::ofstream::binary);

    // save header
    std::size_t N = nodes.size();
    ofs.write(reinterpret_cast<char *>(&N), sizeof(N));

    // save nodes
    for (auto nodeShPtr : nodes) {
        write_node(ofs, nodeShPtr.get());
    }

    // save neighbors
    for (auto neighbors : nodeNeighbors) {
        std::size_t numNeighbors = neighbors.size();
        ofs.write(reinterpret_cast<char *>(&numNeighbors), sizeof(numNeighbors));
        for (auto nodeIdx : neighbors) {
            ofs.write(reinterpret_cast<char *>(&nodeIdx), sizeof(nodeIdx));
        }
    }

    ofs.close();
}

void NSW::load(const std::string& filePath) {
    std::ifstream ifs(filePath, std::ifstream::binary);

    // load header
    std::size_t N;
    ifs.read(reinterpret_cast<char *>(&N), sizeof(N));

    // load nodes
    nodes.resize(N);
    for (std::size_t idx = 0; idx < N; ++idx) {
        nodes[idx] = NodeShPtr(new Node());
        read_node(ifs, const_cast<Node *>(nodes[idx].get()));
    }

    // load neighbors
    nodeNeighbors.resize(N);
    for (std::size_t idx = 0; idx < N; ++idx) {
        std::size_t numNeighbors;
        ifs.read(reinterpret_cast<char *>(&numNeighbors), sizeof(numNeighbors));
        nodeNeighbors[idx].resize(numNeighbors);
        ifs.read(reinterpret_cast<char *>(&nodeNeighbors[idx][0]), numNeighbors * sizeof(nodeNeighbors[idx][0]));
    }

    ifs.close();
}

}
