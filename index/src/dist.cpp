#include <dist.h>
#include <cmath>

namespace nsw {

float Distance_l1::operator() (const Node* node1, const Node* node2) {
    const auto& vec1 = node1->getCoord();
    const auto& vec2 = node2->getCoord();
    float dist = 0;
    for (std::size_t i = 0; i < vec1.size(); ++i) {
        dist += std::abs(vec1[i] - vec2[i]);
    }
    return dist;
}

float Distance_l2::operator() (const Node* node1, const Node* node2) {
    const auto& vec1 = node1->getCoord();
    const auto& vec2 = node2->getCoord();
    float dist = 0;
    for (std::size_t i = 0; i < vec1.size(); ++i) {
        dist += (vec1[i] - vec2[i]) * (vec1[i] - vec2[i]);
    }
    return std::sqrt(dist);
}

}
