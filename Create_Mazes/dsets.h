/* Your code here! */
#pragma once
#include <vector>
using namespace std;

class DisjointSets {
    public:
        int size(int elem);
        void addelements(int num);
        int find(int elem);
        void setunion(int a, int b);

    private:
        vector<int> list;
}; 