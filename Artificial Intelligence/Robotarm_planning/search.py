# search.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
# 
# Created by Jongdeog Lee (jlee700@illinois.edu) on 09/12/2018

"""
This file contains search functions.
"""
# Search should return the path and the number of states explored.
# The path should be a list of tuples in the form (alpha, beta, gamma) that correspond
# to the positions of the path taken by your search algorithm.
# Number of states explored should be a number.
# maze is a Maze object based on the maze from the file specified by input filename
# searchMethod is the search method specified by --method flag (bfs,dfs,greedy,astar)
# You may need to slight change your previous search functions in MP1 since this is 3-d maze


def angleToIdx(angles, offsets, granularity):
    result = []
    for i in range(len(angles)):
        result.append(int((angles[i]-offsets[i]) / granularity))
    return tuple(result)

def idxToAngle(index, offsets, granularity):
    result = []
    for i in range(len(index)):
        result.append(int((index[i]*granularity)+offsets[i]))
    return tuple(result)



def search(maze, searchMethod):
    return {
        "bfs": bfs,
        "dfs": dfs,
        "greedy": greedy,
        "astar": astar,
    }.get(searchMethod, [])(maze)


def bfs_1d(maze):
    ncol = maze.getDimensions()[0]
    granularity = maze.granularity
    offsets = maze.offsets
    visited = [0 for i in range(ncol)]
    

    start_point = maze.getStart() ## this is a tuple
    queue = [[start_point]]
    goals = maze.getObjectives()  ## this is a list
    states_explored = 0

    while queue:
        current_angle = queue[0][-1]
        current_path = queue[0]
        queue.pop(0)
        for next_angle in maze.getNeighbors(current_angle[0]):
            next_alpha = next_angle[0]

            next_position_in_maze = angleToIdx(next_angle, offsets, granularity)
            
            if next_angle in goals:
                return current_path + [next_angle], states_explored
                
            if maze.isValidMove(next_alpha) and visited[next_position_in_maze[0]] == 0:
                states_explored += 1
                visited[next_position_in_maze[0]] = 1
                queue.append(current_path + [next_angle]) 
 
    return [], states_explored


def bfs_2d(maze):
    nrow, ncol = maze.getDimensions()
    granularity = maze.granularity
    offsets = maze.offsets
    
    visited = [[0 for i in range(ncol)] for i in range(nrow)] 
    

    start_point = maze.getStart() ## this is a tuple
    queue = [[start_point]]
    goals = maze.getObjectives()  ## this is a list
    states_explored = 0

    while queue:
        current_angle = queue[0][-1]
        current_path = queue[0]
        queue.pop(0)

        for next_angle in maze.getNeighbors(current_angle[0], current_angle[1]):

            next_alpha = next_angle[0]
            next_beta = next_angle[1]
            next_position_in_maze = angleToIdx(next_angle, offsets, granularity)
        
            if next_angle in goals:
                return current_path + [next_angle], states_explored
                
            if maze.isValidMove(next_alpha, next_beta) and visited[next_position_in_maze[0]][next_position_in_maze[1]] == 0:
                states_explored += 1
                visited[next_position_in_maze[0]][next_position_in_maze[1]] = 1
                queue.append(current_path + [next_angle]) 
 
    return [], states_explored


def bfs_3d(maze):
    nrow, ncol, length = maze.getDimensions()
    granularity = maze.granularity
    offsets = maze.offsets
    
    visited = [[[0 for i in range(length)] for j in range(ncol)] for k in range(nrow)]
    

    start_point = maze.getStart() ## this is a tuple
    queue = [[start_point]]
    goals = maze.getObjectives()  ## this is a list
    states_explored = 0

    while queue:
        current_angle = queue[0][-1]
        current_path = queue[0]
        queue.pop(0)

        for next_angle in maze.getNeighbors(current_angle[0], current_angle[1], current_angle[2]):

            next_alpha = next_angle[0]
            next_beta = next_angle[1]
            next_gamma = next_angle[2]
            next_position_in_maze = angleToIdx(next_angle, offsets, granularity)
        
            if next_angle in goals:
                return current_path + [next_angle], states_explored
                
            if maze.isValidMove(next_alpha, next_beta, next_gamma)\
                 and visited[next_position_in_maze[0]][next_position_in_maze[1]][next_position_in_maze[2]] == 0:
                states_explored += 1
                visited[next_position_in_maze[0]][next_position_in_maze[1]][next_position_in_maze[2]] = 1
                queue.append(current_path + [next_angle]) 
 
    return [], states_explored


def bfs(maze):
    # TODO: Write your code here    
    if len(maze.offsets) == 1:
        print(bfs_1d(maze))
        return bfs_1d(maze)

    elif len(maze.offsets) == 2:
        return bfs_2d(maze)
    
    elif len(maze.offsets) == 3:
        return bfs_3d(maze)

    else:
        print("number of arm links is illegal")
        return [], 0




























    # nrow, ncol = maze.getDimensions()
    # granularity = maze.granularity
    # offsets = maze.offsets
    
    # visited = [[0 for i in range(ncol)] for i in range(nrow)] 
    

    # start_point = maze.getStart() ## this is a tuple
    # queue = [[start_point]]
    # goals = maze.getObjectives()  ## this is a list
    # states_explored = 0

    # while queue:
    #     current_angle = queue[0][-1]
    #     current_path = queue[0]
    #     queue.pop(0)

    #     for next_angle in maze.getNeighbors(current_angle[0], current_angle[1]):

    #         next_alpha = next_angle[0]
    #         next_beta = next_angle[1]
    #         next_position_in_maze = angleToIdx(next_angle, offsets, granularity)
        
    #         if next_angle in goals:
    #             return current_path + [next_angle], states_explored
                
    #         if maze.isValidMove(next_alpha, next_beta) and visited[next_position_in_maze[0]][next_position_in_maze[1]] == 0:
    #             states_explored += 1
    #             visited[next_position_in_maze[0]][next_position_in_maze[1]] = 1
    #             queue.append(current_path + [next_angle]) 
 
    # return [], states_explored





































def dfs(maze):
    # TODO: Write your code here    
    return [], 0

def greedy(maze):
    # TODO: Write your code here    
    return [], 0

def astar(maze):
    # TODO: Write your code here    
    return [], 0