/**
 * @file kdtree.cpp
 * Implementation of KDTree class.
 */

#include <utility>
#include <algorithm>
#include <iostream>
#include <string>
using std::cout;
using std::endl;
using namespace std;

template <int Dim>
bool KDTree<Dim>::smallerDimVal(const Point<Dim>& first,
                                const Point<Dim>& second, int curDim) const
{
    /**
     * @todo Implement this function!
     */
    if (curDim >= Dim) {
      return true;
    }
    if (first[curDim] < second[curDim]) return true;
    if (first[curDim] == second[curDim]) return first < second;
    return false;
}

template <int Dim>
bool KDTree<Dim>::shouldReplace(const Point<Dim>& target,
                                const Point<Dim>& currentBest,
                                const Point<Dim>& potential) const
{
    /**
     * @todo Implement this function!
     */
    int dim = 0;
    int distanceBest = 0;
    int distancePotential = 0;

    while (dim < Dim) {
      distanceBest += (target[dim] - currentBest[dim]) * (target[dim] - currentBest[dim]);
      distancePotential += (target[dim] - potential[dim]) * (target[dim] - potential[dim]);
      dim++;
    }
    if (distanceBest == distancePotential) return potential < currentBest;
    return distancePotential < distanceBest;
}



template <int Dim>
KDTree<Dim>::KDTree(const vector<Point<Dim>>& newPoints)
{
    /**
     * @todo Implement this function!
     */
  if (newPoints.empty()) {
    root = new KDTreeNode();
    return;
  }
  vector<Point<Dim>> copy = newPoints;
  root = buildTree(copy, 0, newPoints.size() - 1, 0);
}

template <int Dim>
KDTree<Dim>::KDTree(const KDTree<Dim>& other) {
  /**
   * @todo Implement this function!
   */
  root = copyNode(other.root);
}

template <int Dim>
const KDTree<Dim>& KDTree<Dim>::operator=(const KDTree<Dim>& rhs) {
  /**
   * @todo Implement this function!
   */
  if (root != NULL) deleteNode(root);
  root = copyNode(rhs.root);
  return *this;
}

////////////////////////////// Helper deleteNode
template <int Dim>
void KDTree<Dim>::deleteNode(KDTreeNode * current) {
  if (current == NULL) return; 
  deleteNode(current -> left);
  deleteNode(current -> right);
  delete current;
  current = NULL;
}


/////////////////////////////Helper buildTree
template <int Dim>
typename KDTree<Dim>::KDTreeNode* KDTree<Dim>::buildTree(vector<Point<Dim>> & points, int start, int end, int dim_to_select) {
  if (start > end) return NULL;
  if (start == end) {
    typename KDTree<Dim>::KDTreeNode* node = new KDTree<Dim>::KDTreeNode(points[start]);
    return node;
  }
  int median = (start + end) / 2;
  typename KDTree<Dim>::KDTreeNode* newNode = new KDTree<Dim>::KDTreeNode(quickSelect(points, start, end, dim_to_select, median));
  newNode -> left = buildTree(points, start, median - 1, (dim_to_select + 1) % Dim);
  newNode -> right = buildTree(points, median + 1, end,  (dim_to_select + 1) % Dim);
  return newNode;
   
}

//////////////////////////////Helper quickselect
template <int Dim>
Point<Dim> & KDTree<Dim>::quickSelect(vector<Point<Dim>> & points, int start, int end, int dim_to_select, int median) {
  if (start == end) return points[start];
  int paritioner = partition(points, start, end, dim_to_select);
  if (paritioner == median) return points[median];
  else if (paritioner < median) return quickSelect(points, paritioner + 1, end, dim_to_select, median);
  else return quickSelect(points, start, paritioner - 1, dim_to_select, median);
  
}

////////////////////////////////Helper partition
template <int Dim>
int KDTree<Dim>::partition(vector<Point<Dim>> & points, int start, int end, int dim_to_select) {
  if (start >= end) return start;
  int pivotValue = points[start][dim_to_select];
  int pivot = start;
  for (int i = start + 1; i <= end; i++) {
    if (points[i][dim_to_select] < pivotValue 
      || (points[i][dim_to_select] == pivotValue && points[i] < points[start])) {
        pivot++;
        swap(points, i, pivot);
      }
  }
  swap(points, pivot, start);
  return pivot;
}

/////////////////////////////// global Helper swap
template <int Dim>
void swap(vector<Point<Dim>> & points, int index1, int index2) {
  Point<Dim> temp =  points[index1];
  points[index1] = points[index2];
  points[index2] = temp;
}



/////////////////////////////Helper copyNode
template <int Dim>
typename KDTree<Dim>::KDTreeNode* KDTree<Dim>::copyNode(KDTreeNode * otherRoot) {
  if (otherRoot == NULL) return;
  KDTreeNode * newNode = new KDTreeNode(*otherRoot);
  newNode -> left = copyNode(otherRoot -> left);
  newNode -> right = copyNode(otherRoot -> right);
  return newNode;
}

template <int Dim>
KDTree<Dim>::~KDTree() {
  /**
   * @todo Implement this function!
   */
  // cout << "destructor " << endl;
  deleteNode(root);
}

template <int Dim>
Point<Dim> KDTree<Dim>::findNearestNeighbor(const Point<Dim>& query) const
{
    /**
     * @todo Implement this function!
     */
    if (root == NULL) return Point<Dim>();
    Point<Dim> tempBest = root -> point;
    // cout << "(" << query[0] << ", " << query[1] << ", " << query[2] << ")";
    return findNearest(root, query, tempBest, 0); 
}

//////////////////////////// Helper findNeaerest 
template <int Dim>
Point<Dim> KDTree<Dim>::findNearest(KDTreeNode* current, const Point<Dim>& target,
                                  Point<Dim> & tempBest, int dim_to_check) const {
  if (current == NULL) {
    return tempBest;
  }
  if (target[dim_to_check] < current -> point[dim_to_check] 
    || (target[dim_to_check] == current -> point[dim_to_check] && target < current -> point)) {
    tempBest = findNearest(current -> left, target, tempBest, (dim_to_check + 1) % Dim);
  } else if (target[dim_to_check] > current -> point[dim_to_check] 
    || (target[dim_to_check] == current -> point[dim_to_check] && target > current -> point)) {
    tempBest = findNearest(current -> right, target, tempBest, (dim_to_check + 1) % Dim);
  } else {
    tempBest = current -> point;
  }

  if (shouldReplace(target, tempBest, current -> point)) {
    tempBest = current -> point;
  }

  // cout << tempBest[0] << endl;
  double radius = getRadius(target, tempBest);
  // cout <<  "current = (" << current -> point[0] << ", " << current -> point[1] << ", " << current -> point[2] << ")";
  // cout << "best = (" << tempBest[0] << ", " << tempBest[1] <<", " << tempBest[2] << ")";
  // cout << "r = " << radius << endl;
  if (radius >= abs(current -> point[dim_to_check] - target[dim_to_check])) {
    Point<Dim> bestOtherSide = (target[dim_to_check] < current -> point[dim_to_check] 
            || (target[dim_to_check] == current -> point[dim_to_check] && target < current -> point)) ?
             findNearest(current -> right, target, tempBest, (dim_to_check + 1) % Dim) :
             findNearest(current -> left, target, tempBest, (dim_to_check + 1) % Dim);
    tempBest = shouldReplace(target, tempBest, bestOtherSide) ? bestOtherSide : tempBest;
  }

  return tempBest;
  
}

//////////////////////////global helper getRadius
template <int Dim>
double getRadius(Point<Dim> A, Point<Dim> B) {
  int dim = 0;
  double radius = 0;
  while (dim < Dim) {
    radius += (A[dim] - B[dim]) * (A[dim] - B[dim]);
    dim++;
  }
  return sqrt(radius);
}













