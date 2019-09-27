/* Your code here! */
#pragma once
#include <vector>
#include "cs225/PNG.h"
#include <iostream>
#include <stack>
#include <queue>
#include <tuple>
#include "dsets.h"
using namespace std;
using namespace cs225;
using cs225::PNG;
class SquareMaze {
  public:
    SquareMaze() {};
    void makeMaze(int width_, int height_);
    bool canTravel(int x, int y, int dir) const;
    void setWall(int x, int y, int dir, bool exists);
    vector<int> solveMaze();
    PNG * drawMaze() const;
    PNG * drawMazeWithSolution();


  private:
    vector<bool> rightWall;
    vector<bool> downWall;
    int width;
    int height;
    static bool has_seed;
    
};