/* Your code here! */
#include "maze.h"
bool SquareMaze::has_seed = false;
void SquareMaze::makeMaze(int width_, int height_) {
    width = width_;
    height = height_;
    if (!has_seed) {
        srand(time(NULL));
        has_seed = true;
    }
    if (!rightWall.empty() || !downWall.empty()) {
        rightWall.clear();
        downWall.clear();
    }

    for (int x = 0; x < width; x++) {
        for (int y = 0; y < height; y++) {
            rightWall.push_back(true);
            downWall.push_back(true);
        }
    }

    DisjointSets set;
    set.addelements(width * height);
    int count = 0;
    while (count < width * height - 1) {
        int direction = rand() % 2;
        int index = rand() % (width * height);
        int x = index % width;
        int y = index / height;
        if (direction == 0) {
            if (x == width - 1) continue;
            if (set.find(index) != set.find(index + 1)) {
                setWall(x, y, 0, false);
                set.setunion(index, index + 1);
                count++;
            }
        } else if (direction == 1) {
            if (y == height - 1) continue;
            if (set.find(index) != set.find(index + width)) {
                setWall(x, y, 1, false);
                set.setunion(index, index + width);
                count++;
            }
        }
    }
}

bool SquareMaze::canTravel(int x, int y, int dir) const {
    switch (dir)
    {
        case 0:
            if (x + 1 >= width || rightWall[x + y * width]) return false;
            return true;
        case 1:
            if (y + 1 >= height || downWall[x + y * width]) return false;
            return true;
        case 2:
            if (x - 1 < 0 || rightWall[y * width + x - 1]) return false;
            return true;
        case 3:
            if (y - 1 <  0 || downWall[(y - 1)* width + x]) return false;
            return true;
        default:
            break;
    }
    return false;
}

void SquareMaze::setWall(int x, int y, int dir, bool exists) {
    if (dir == 0) {
        rightWall[x + y * width] = exists; 
    } else if (dir == 1) {
        downWall[x + y * width] = exists;  
    } 
}


std::vector<int> SquareMaze::solveMaze() {
    vector<tuple<int, int, int>> data(width * height, make_tuple(-1,-1,-1));
    queue<int> bfs;
    bfs.push(0);
    while (!bfs.empty()) {
        int prev = bfs.front();
        bfs.pop();
        int x = prev % width;
        int y = prev / width;
        
        if (canTravel(x, y, 0)) {
            if (get<0>(data[prev + 1]) == -1) {
                get<0>(data[prev + 1]) = get<0>(data[prev]) + 1;
                get<1>(data[prev + 1]) = 0;
                get<2>(data[prev + 1]) = prev;
                bfs.push(prev + 1);
            }
        }

        if (canTravel(x, y, 1)) {
            if (get<0>(data[prev + width]) == -1) {
                get<0>(data[prev + width]) = get<0>(data[prev]) + 1;
                get<1>(data[prev + width]) = 1;
                get<2>(data[prev + width]) = prev;
                bfs.push(prev + width);
            }
        }

        if (canTravel(x, y, 2)) {
            if (get<0>(data[prev -1]) == -1) {
                get<0>(data[prev - 1]) = get<0>(data[prev]) + 1;
                get<1>(data[prev - 1]) = 2;
                get<2>(data[prev - 1]) = prev;
                bfs.push(prev - 1);
            }
        }

        if (canTravel(x, y, 3)) {
            if (get<0>(data[prev - width]) == -1) {
                get<0>(data[prev - width]) = get<0>(data[prev]) + 1;
                get<1>(data[prev - width]) = 3;
                get<2>(data[prev - width]) = prev;
                bfs.push(prev - width);
            }
        }
    }

    int desntination = 0;
    for (int i = 1 + width * (height - 1); i < width * height; i++) {
        if (get<0>(data[i]) > get<0>(data[desntination])) {
            desntination = i;
        }
    }

    vector<int> path;
    while (desntination > 0) {
        path.insert(path.begin(), get<1>(data[desntination]));
        desntination = get<2>(data[desntination]);
    }
    return path;
    
}

PNG * SquareMaze::drawMaze() const {
    PNG * maze_png = new PNG(width * 10 +  1, height * 10 + 1);
    HSLAPixel black = HSLAPixel(0, 0, 0);
    for (int i = 0; i <= height * 10; i++) {
        HSLAPixel & temp = maze_png -> getPixel(0, i);
        temp = black;
    }
    for (int j = 10; j <= width * 10; j++) {
        HSLAPixel & temp = maze_png -> getPixel(j, 0);   
        temp = black;
    }
    for (int x = 0; x < width; x++) {
        for (int y = 0; y < height; y++) {
            if (x == width - 1 || rightWall[x + y * width]) {
                for (int i = 0; i <= 10; i++) {
                    maze_png -> getPixel((x + 1) * 10, y * 10 + i) = black;
                }
            } 
            if (y == height - 1 || downWall[x + y * width]) {
                for (int i = 0; i <= 10; i++) {
                    maze_png -> getPixel(x * 10 + i, (y + 1) * 10) = black;
                }
            }
        }
    }
    return  maze_png;
}
    

PNG * SquareMaze::drawMazeWithSolution() {
    PNG * maze = drawMaze();
    vector<int> path = solveMaze();
    int x = 5, y = 5;
    HSLAPixel white = HSLAPixel(360, 1, 1);
    HSLAPixel red = HSLAPixel(360, 1, 0.5);
    for (unsigned i = 0; i < path.size(); i++) {
        switch (path[i]) {
            case 0:
                for (int j = 0; j <= 10; j++) {
				    maze->getPixel(x + j, y) = red;
			    }
			    x += 10;
                break;
            case 1:
                for (int j = 0; j <= 10; j++) {
				    maze->getPixel(x, y + j) = red;
			    }
			    y += 10;
                break;
            case 2:
                for (int j = 0; j <= 10; j++) {
				    maze->getPixel(x - j, y) = red;
			    }
			    x -= 10;
                break;
            case 3:
                for (int j = 0; j <= 10; j++) {
				    maze->getPixel(x, y - j) = red;
			    }
			    y -= 10;
                break;
            default:
                break;
        }
    }
    x -= 5;
    y += 5;
    for (int k = 1; k < 10; k++) {
        maze -> getPixel(x + k, y) = white;
    }
    return maze;
}