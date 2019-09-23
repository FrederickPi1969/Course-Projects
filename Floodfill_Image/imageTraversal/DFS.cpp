#include <iterator>
#include <cmath>

#include <list>
#include <queue>
#include <stack>
#include <vector>

#include <iostream>
#include <string>
#include "../cs225/PNG.h"
#include "../Point.h"

#include "ImageTraversal.h"
#include "DFS.h"
using std::vector;
using std::cout;
using std::endl;



/**
 * Initializes a depth-first ImageTraversal on a given `png` image,
 * starting at `start`, and with a given `tolerance`.
 *
 * @param png The image this DFS is going to traverse
 * @param start The start point of this DFS
 * @param tolerance If the current point is too different (difference larger than tolerance) with the start point,
 * it will not be included in this DFS
 std::vector<Point> alreadyVisited;
 std::stack<Point> toVisit;
 */
DFS::DFS(const PNG & png, const Point & start, double tolerance) {
    /** @todo [Part 1] */
    picture = png;
    startPoint = start;
    bound = tolerance;

    for (unsigned int i = 0; i < picture.width(); i++) {
        std::vector<bool> row;
        for (unsigned int j = 0; j < picture.height(); j++) {
            row.push_back(false);
        }
        visitmap.push_back(row);
        current.push_back(row);
    }

    if (startPoint.x < picture.width() && startPoint.y < picture.height()) {
        s.push(startPoint);
        visitmap[start.x][start.y] = true;
        current[start.x][start.y] = true;
    }
}

/**
 * Returns an iterator for the traversal starting at the first point.
 */
ImageTraversal::Iterator DFS::begin() {
  /** @todo [Part 1] */
  return ImageTraversal::Iterator(this);
}

/**
 * Returns an iterator for the traversal one past the end of the traversal.
 */
ImageTraversal::Iterator DFS::end() {
  /** @todo [Part 1] */
  return ImageTraversal::Iterator();
}


bool checkAround(Point & point, PNG & picture, vector<vector<bool>> visitmap, Point startPoint, double bound) {
  HSLAPixel & start = picture.getPixel(startPoint.x, startPoint.y);
  if (point.x + 1 < picture.width()) {
    HSLAPixel & right = picture.getPixel(point.x + 1, point.y);
    if (ImageTraversal::calculateDeltaHelper(right, start) <= bound && !visitmap[point.x + 1][point.y]) {
      return true;
    }
  }
  if (point.y + 1 < picture.height()) {
    HSLAPixel & up = picture.getPixel(point.x, point.y + 1);
    if (ImageTraversal::calculateDeltaHelper(up, start) <= bound && !visitmap[point.x][point.y + 1]) {
      return true;
    }
  }
  if ((int) point.x - 1 >= 0) {
    HSLAPixel &  left = picture.getPixel((int) point.x - 1, point.y);
    if (ImageTraversal::calculateDeltaHelper(left, start) <= bound && !visitmap[(int)point.x - 1][point.y]) {
      return true;
    }
  }
  if ((int) point.y - 1 >= 0) {
    HSLAPixel & down = picture.getPixel(point.x, (int) point.y - 1);
    if (ImageTraversal::calculateDeltaHelper(down, start) <= bound && !visitmap[point.x][(int)point.y - 1]) {
      return true; 
    }
  }
  return true;
}
/**
 * Adds a Point for the traversal to visit at some point in the future.
 */
void DFS::add(const Point & point) {
    /** @todo [Part 1] */
  if (point.x < picture.width() && point.y < picture.height()) {
    if (!visitmap[point.x][point.y]) {
        HSLAPixel & start = picture.getPixel(startPoint.x, startPoint.y);
        HSLAPixel & temp = picture.getPixel(point.x, point.y);
        if (ImageTraversal::calculateDeltaHelper(temp, start) <= bound) {
            s.push(point);
            visitmap[point.x][point.y] = true;
            current[point.x][point.y] = true;
        }
    } else {
        if (current[point.x][point.y]) {
            s.push(point);
        }
    }
  }
}

/**
 * Removes and returns the current Point in the traversal.
 */
Point DFS::pop() {
  /** @todo [Part 1] */
  if (s.empty()) {
      return Point(-1, -1);
  }
  Point temp = s.top();
  while (!current[temp.x][temp.y]) {
    s.pop();
    if (s.empty()) {
      return Point(-1, -1);
    }
    temp = s.top();
  }
  current[temp.x][temp.y] = false;
  s.pop();
  return temp;
}

/**
 * Returns the current Point in the traversal.
 */
Point DFS::peek() const {
  /** @todo [Part 1] */
  if (s.empty()) {
    return Point(-1, -1);
  }
  Point temp = s.top();
  while (!current[temp.x][temp.y]) {
    const_cast<DFS *>(this) -> s.pop();
     if (s.empty()) {
        return Point(-1, -1);
    }
    temp = s.top();
  }
  // while (!checkAround(temp, const_cast<DFS *>(this) -> picture, visitmap, startPoint, bound)) {
  //   const_cast<DFS *>(this) -> s.pop();
  //   if (s.empty()) {
  //     return Point(-1, -1);
  //   }
  //   temp = s.top();
  // }
  return temp;
}

/**
 * Returns true if the traversal is empty.
 */
bool DFS::empty() const {
  /** @todo [Part 1] */
  return s.empty();
}