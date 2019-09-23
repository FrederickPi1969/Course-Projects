/* Your code here! */
#include "dsets.h"

int DisjointSets::size(int elem) {
    int representation = find(elem);
    return 0 - list[representation];
}

void DisjointSets::addelements(int num) {
    for (int i = num; i >= 1; i--) {
        list.push_back(-1);
    } 
}

int DisjointSets::find(int elem) {
    if (list[elem] < 0) return elem;
    list[elem] = find(list[elem]);
    return list[elem];
}

void DisjointSets::setunion(int a, int b) {
    int root1 = find(a);
    int root2 = find(b);
    int size = list[root1] + list[root2];
    if (0 - list[root1] > 0 - list[root2]) {
        list[root2] = root1;
        list[root1] = size; 
    } else {
        list[root1] = root2;
        list[root2] = size;
    }
}