#include <cmath>

#include <list>
#include <queue>
#include <stack>
#include <vector>

#include "../cs225/PNG.h"
#include "../Point.h"

#include "ImageTraversal.h"
#include "BFS.h"

using namespace cs225;

/**
 * Initializes a breadth-first ImageTraversal on a given `png` image,
 * starting at `start`, and with a given `tolerance`.
 * @param png The image this BFS is going to traverse
 * @param start The start point of this BFS
 * @param tolerance If the current point is too different (difference larger than tolerance) with the start point,
 * it will not be included in this BFS
 */
BFS::BFS(const PNG & png, const Point & start, double tolerance) {
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
  }

  if (startPoint.x < picture.width() && startPoint.y < picture.height()) {
      q.push(startPoint);
      visitmap[startPoint.x][startPoint.y] = true;
  }
}

/**
 * Returns an iterator for the traversal starting at the first point.
 */
ImageTraversal::Iterator BFS::begin() {
  /** @todo [Part 1] */
  return ImageTraversal::Iterator(this);
}

/**
 * Returns an iterator for the traversal one past the end of the traversal.
 */
ImageTraversal::Iterator BFS::end() {
  /** @todo [Part 1] */
  return ImageTraversal::Iterator();
}

/**
 * Adds a Point for the traversal to visit at some point in the future.
 */
void BFS::add(const Point & point) {
  /** @todo [Part 1] */
  if (point.x < picture.width() && point.y < picture.height() && !visitmap[point.x][point.y]) {
    HSLAPixel & start = picture.getPixel(startPoint.x, startPoint.y);
    HSLAPixel & temp = picture.getPixel(point.x, point.y);
    if (ImageTraversal::calculateDeltaHelper(temp, start) <= bound) {
      q.push(point);
      visitmap[point.x][point.y] = true;
    }
  }
}

/**
 * Removes and returns the current Point in the traversal.
 */
Point BFS::pop() {
  /** @todo [Part 1] */
  if (q.empty()) {
    return Point(-1, -1);
  }
  Point temp = q.front();
  q.pop();
  return temp;
}

/**
 * Returns the current Point in the traversal.
 */
Point BFS::peek() const {
  /** @todo [Part 1] */
  return q.empty() ? Point(-1, -1) : q.front();
}

/**
 * Returns true if the traversal is empty.
 */
bool BFS::empty() const {
  /** @todo [Part 1] */
  return q.empty();
}