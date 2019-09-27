# CS 440 MP2: Robotic Arm


## Description

This program helps a robot arm to find the shortest path to reach its goal. The arms have granularity, which can be used to transform the motion of n arms into a n-D matrix. With some algorithm, the transformation speed is improved a great deal.


####  Examples
- When there's a single arm:
<img src="onelink.jpg">

- The two arm links case:  
  
    
<img src="twolinks.jpg">

- And the three arm links case:
<img src="threelinks.jpg">


The transformed 2-D maze looks like this:
<img src="twoArmMaze.jpg">








## Implement:
1. geometry.py
2. transform.py
3. search.py
4. maze.py 
## Requirements:
```
python3
pygame
numpy (optional)
```
## Running:
The main file to run the mp is mp1.py:

```
usage: mp2.py [-h] [--map MAP_NAME] [--method {bfs,dfs,greedy,astar}]
              [--human] [--fps FPS] [--granularity GRANULARITY]
              [--trajectory TRAJECTORY] [--save-image SAVEIMAGE]
              [--save-maze SAVEMAZE]
```

Examples of how to run MP2:
```
python mp2.py --map Map1 --human
```
```
python mp1.py --map Map2 --granularity 10 --method astar
```

For help run:
```
python mp2.py -h
```
Help Output:
```
CS440 MP2 Robotic Arm

optional arguments:
  -h, --help            show this help message and exit
  --map MAP_NAME        configuration filename - default BasicMap
  --method {bfs,dfs,greedy,astar}
                        search method - default bfs
  --human               flag for human playable - default False
  --fps FPS             fps for the display - default 30
  --granularity GRANULARITY
                        degree granularity - default 2
  --trajectory TRAJECTORY
                        leave footprint of rotation trajectory in every x
                        moves - default 0
  --save-image SAVEIMAGE
                        save output to image file - default not saved
  --save-maze SAVEMAZE  save the contructed maze to maze file - default not
                        saved

```