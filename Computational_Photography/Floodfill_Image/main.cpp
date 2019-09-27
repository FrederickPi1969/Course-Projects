
#include "cs225/PNG.h"
#include "FloodFilledImage.h"
#include "Animation.h"

#include "imageTraversal/DFS.h"
#include "imageTraversal/BFS.h"

#include "colorPicker/RainbowColorPicker.h"
#include "colorPicker/GradientColorPicker.h"
#include "colorPicker/GridColorPicker.h"
#include "colorPicker/SolidColorPicker.h"
#include "colorPicker/MyColorPicker.h"
#include <iostream>
using std::cout;
using namespace cs225;

int main() {

  // @todo [Part 3]
  // - The code below assumes you have an Animation called `animation`
  // - The code provided below produces the `myFloodFill.png` file you must
  //   submit Part 3 of this assignment -- uncomment it when you're ready.
  //
  //
  PNG bgImage = PNG();
  bgImage.readFromFile("pacman.png");
  FloodFilledImage module = FloodFilledImage(bgImage);
  Point startPoint = Point(100, 100);

  DFS dfs1 = DFS(bgImage, startPoint, 0.18);
  MyColorPicker sincos = MyColorPicker(bgImage);
  module.addFloodFill(dfs1, sincos);
  Animation animation = module.animate(200);


  DFS dfs2 = DFS(bgImage, startPoint, 0.18);
  RainbowColorPicker rainbow = RainbowColorPicker(30);
  module.addFloodFill(dfs2, rainbow);
  Animation anime = module.animate(200);

  for (int i = 0; i < (int)anime.frameCount(); i++) {
      animation.addFrame(anime.getFrame(i));
  }

  PNG last = anime.getFrame(anime.frameCount() - 1);
  animation.write("myFloodFill.gif");
  last.writeToFile("myFloodFill.png");

  return 0xdeadbeef;
}
