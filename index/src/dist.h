#pragma once

#include <node.h>
#include <vector>

namespace nsw {

class Distance {
public:
    Distance() {};
    virtual ~Distance() {};
    virtual float operator() (const Node* node1, const Node* node2) = 0;
};

class Distance_l1: public Distance {
public:
    float operator() (const Node* node1, const Node* node2);
};

class Distance_l2: public Distance {
public:
    float operator() (const Node* node1, const Node* node2);
};

}
