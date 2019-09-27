/**
 * @file maptiles.cpp
 * Code for the maptiles function.
 */

#include <iostream>
#include <map>
#include "maptiles.h"
//#include "cs225/RGB_HSL.h"

using namespace std;


Point<3> convertToXYZ(LUVAPixel pixel) {
    return Point<3>( pixel.l, pixel.u, pixel.v );
}

MosaicCanvas* mapTiles(SourceImage const& theSource,
                       vector<TileImage>& theTiles)
{
    /**
     * @todo Implement this function!
     */
    MosaicCanvas * output = new MosaicCanvas(theSource.getRows(), theSource.getColumns());
    map<Point<3>, int>  map;
    vector<Point<3>> colorList;
    for (unsigned i = 0; i < theTiles.size(); i++) {
      LUVAPixel color_in_point = theTiles[i].getAverageColor();
      Point<3>  averageColor = convertToXYZ(color_in_point);
      colorList.push_back(averageColor);
    }

    KDTree<3> tree(colorList);

    vector<Point<3>>::iterator it = colorList.begin();
    int count = 0;
    while (it != colorList.end()) {
      map[*it] = count;
      it++;
      count++;
    }

    for (int x = 0; x < theSource.getRows(); x++) {
      for (int y = 0; y < theSource.getColumns(); y++) {
        Point<3> target = convertToXYZ(theSource.getRegionColor(x, y));
        Point<3> key = tree.findNearestNeighbor(target);
        int index = map.at(key);
        output -> setTile(x, y, &theTiles[index]);
      }
    }

    return output;
}
