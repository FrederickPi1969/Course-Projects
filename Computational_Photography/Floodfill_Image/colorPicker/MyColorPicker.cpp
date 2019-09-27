#include "../cs225/HSLAPixel.h"
#include "../Point.h"

#include "ColorPicker.h"
#include "MyColorPicker.h"
#include "../cs225/PNG.h"
#include  <math.h>
#include <cmath>
using namespace cs225;

/**
 * Picks the color for pixel (x, y).
 * Using your own algorithm
 */

MyColorPicker::MyColorPicker(PNG image) : picture(image){};
HSLAPixel MyColorPicker::getColor(unsigned x, unsigned y) {
  /* @todo [Part 3] */
  int x1 = 0;  // start x
  int y1 = 0;  //start y;
  int x3 = picture.width() - 1; // end x
  int y3 = 0;  // end y
  int x2 = picture.width() / 2;
  int y2 = picture.height() - 1;   /// middle point;

  double b = ((y1-y3)*(x1*x1-x2*x2)-(y1-y2)*(x1*x1-x3*x3))/((x1-x3)*(x1*x1-x2*x2)-(x1-x2)*(x1*x1-x3*x3));
  double a = ((y1-y2)-b*(x1-x2))/(x1*x1-x2*x2);
  double c = ((y1-y2)-b*(x1-x2))/(x1*x1-x2*x2);
  int correspondY = a*x*x + b*x + c;

  double h = 360;
  double l = 1;
  double s = 1;
  if ((int) y == correspondY) {

    return HSLAPixel(h, s, l);

  } else if ((int)y < correspondY) {

    h -= ((double) correspondY / 360) * (correspondY - y);
    l -= (1 / (2 * (double) correspondY)) * (correspondY - y);
    s -= (1 / (2 * (double) correspondY)) * (correspondY - y);

  } else {

    h -= (((double) picture.height() - (double) correspondY) / 360) * (y - correspondY);
    l -=  (1 / (2 * ((double) picture.height() - (double) correspondY))) * (y - correspondY);
    s -=  (1 / (2 * ((double) picture.height() - (double) correspondY))) * (y - correspondY);

  }

  return HSLAPixel(h, s, l);

  // double h = std::abs(360 * sin(((double)x+y) / 16)) + 120;
  // // double h = std::abs(360 * sin(((double)x+y))) ;
  // if (h == 0) {
  //   h = std::abs(360 * cos((double) x + y));
  // } else if (h > 360) {
  //   h -= 120;
  // }
  // return HSLAPixel(h, 0.8, 0.8);

}
