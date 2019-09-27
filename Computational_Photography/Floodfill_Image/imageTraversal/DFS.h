
#pragma once

#include <iterator>
#include <cmath>
#include <list>
#include <stack>
#include <vector>
#include <algorithm>
#include <iostream>

#include "../cs225/PNG.h"
#include "../Point.h"

#include "ImageTraversal.h"
using std::stack;
using namespace cs225;

/**
 * A depth-first ImageTraversal.
 * Derived from base class ImageTraversal
 */
class DFS : public ImageTraversal {
public:
  DFS(const PNG & png, const Point & start, double tolerance);

  ImageTraversal::Iterator begin();
  ImageTraversal::Iterator end();

  void add(const Point & point);
  Point pop();
  Point peek() const;
  bool empty() const;

private:
	/** @todo [Part 1] */
	/** add private members here*/
    stack<Point> s;
    std::vector<std::vector<bool>> visitmap;
    std::vector<std::vector<bool>> current;
    PNG picture;
    Point startPoint;
    double bound;
};