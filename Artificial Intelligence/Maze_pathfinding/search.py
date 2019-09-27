# search.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Michael Abir (abir2@illinois.edu) on 08/28/2018

"""
This is the main entry point for MP1. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""
# Search should return the path.
# The path should be a list of tuples in the form (row, col) that correspond
# to the positions of the path taken by your search algorithm.
# maze is a Maze object based on the maze from the file specified by input filename
# searchMethod is the search method specified by --method flag (bfs,dfs,astar,astar_multi,extra)
import PriorityQueue

# def heuristic(open_list, maze, distance_list, parent_list, goal):
#     min_index = -1
#     min_cost = 999999999
#     for i,elem in enumerate(open_list):
#         current_pos = elem
#         dist_to_start = distance_list[parent_list[current_pos]]
#         dist_to_goal = abs(current_pos[0] - goal[0]) + abs(current_pos[1] - goal[1]) 
#         current_cost = dist_to_start + dist_to_goal 
#         change = current_cost < min_cost
#         min_cost = current_cost if change else min_cost
#         min_index = i if change else min_index 
#     next_step = open_list[min_index]
#     open_list.pop(min_index)
#     return next_step
    


def search(maze, searchMethod):
    return {
        "bfs": bfs,
        "dfs": dfs,
        "astar": astar,
        "astar_multi": astar,
        "extra": astar_multi,
    }.get(searchMethod)(maze)


def bfs(maze):
    """
    Runs BFS for part 1 of the assignment.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here
    print("this is the BFS method")

    nrow = maze.rows
    ncol = maze.cols 
    visited = [[0 for i in range(ncol)] for i in range(nrow)] 
    

    start_point = maze.getStart() ## this is a tuple
    queue = [[start_point]]
    goals = maze.getObjectives()  ## this is a list
    while True:
        current_pos = queue[0][-1]
        current_path = queue[0]
        queue.pop(0)

        for next_position in maze.getNeighbors(current_pos[0], current_pos[1]):

            next_x = next_position[0]
            next_y = next_position[1]

            if next_position in goals:
                return current_path + [next_position]
                

            if maze.isValidMove(next_x, next_y) and visited[next_x][next_y] == 0:
                visited[next_x][next_y] = 1
                queue.append(current_path + [next_position]) 

    return queue[-1]


def print_visited(visited):
    for l in visited:
        print(l)
    print("==========================")


def dfs(maze):
    """
    Runs DFS for part 1 of the assignment.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here
    
    print("this is the DFS method")
    
    
    start_point = maze.getStart() ## this is a tuple
    # stack = [start_point]
    goal = maze.getObjectives()[0]  
    nrow = maze.rows 
    ncol = maze.cols 
    visited = [[0 for i in range(ncol)] for i in range(nrow)] 
    stack = [start_point]
    
    while True:
        movable = False
        current_pos = stack[-1]
        visited[current_pos[0]][current_pos[1]] = 1

        for next_pos in maze.getNeighbors(current_pos[0], current_pos[1]):

            if next_pos == goal:
                return stack + [goal]

            
            next_x = next_pos[0]
            next_y = next_pos[1]
            if maze.isValidMove(next_x, next_y) and visited[next_x][next_y] == 0:
                movable = True
                stack.append(next_pos) 
                break
                # print(stack)

        if not movable:
            stack.pop(-1)

    return []
        

    

#     CURRENT_BEST = [9999999999]
#     BEST_PATH = [None]
#     nrow = maze.rows 
#     ncol = maze.cols 
  
    


# def dfs_recur(maze,current_pos, visited, goal, step_count, path, CURRENT_BEST, BEST_PATH):
#     if step_count >= CURRENT_BEST[0] and current_pos != goal:
#         # visited[current_pos[0]][current_pos[1]] = 1 
#         # path.append(current_pos)
#         # print(CURRENT_BEST[0])
#         path.append(current_pos)
#         return 

#     if current_pos == goal:
#         # path.append(current_pos)
#         # visited[current_pos[0]][current_pos[1]] = 1 
#         print("arrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrived")
#         # change = step_count < CURRENT_BEST[0] 
#         CURRENT_BEST[0] = step_count 
#         path.append(goal) 
#         BEST_PATH[0] = path.copy() 
#         return 

#     else:

#         visited[current_pos[0]][current_pos[1]] = 1
#         path.append(current_pos)
#         for next_pos in maze.getNeighbors(current_pos[0], current_pos[1]):
#             # print(next_pos)
#             if maze.isValidMove(next_pos[0], next_pos[1]) and visited[next_pos[0]][next_pos[1]] == 0:
#                 # path.append(next_pos)
#                 # visited[next_pos[0]][next_pos[1]] = 1
                
#                 # print_visited(visited)    
#                 dfs_recur(maze,next_pos, visited, goal, step_count + 1, path, CURRENT_BEST, BEST_PATH)
#                 # print("ever done")
#                 visited[next_pos[0]][next_pos[1]] = 0
#                 path.pop(-1)
                
    
        
    
    

def astar(maze):
    """
    Runs A star for part 1 of the assignment.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    nrow = maze.rows 
    ncol = maze.cols 
    visited = [[0 for i in range(ncol)] for i in range(nrow)] 
    goal = maze.getObjectives()[0]

    start_point = maze.getStart() ## this is a tuple
    parent_list = {start_point : None}
    distance_list = {start_point : 0}

    q = PriorityQueue.Q_for_maze_single(maze, distance_list, goal)
    q.insert(start_point)
    
    not_arrived = True
    while not_arrived:
        # find most prior one and switch it to closed list. 
        # mark it as visited 
        next_step = q.pop()
        
        for next_pos in maze.getNeighbors(next_step[0], next_step[1]): 
            if maze.isValidMove(next_pos[0], next_pos[1]) and visited[next_pos[0]][next_pos[1]] == 0:
                parent_list[next_pos] = next_step 
                distance_list[next_pos] = distance_list[next_step] + 1 
                visited[next_pos[0]][next_pos[1]] = 1 
                q.insert(next_pos)
            
            if next_pos == goal:
                not_arrived = False 
                break
        
    node = goal
    path = []
    while parent_list[node] != start_point:
        path.insert(0, node)
        node = parent_list[node]
    path.insert(0,node)
    path.insert(0, start_point)
    
    return path
        
def astar_helper(maze, start_point, goal):
    """
    Runs A star for part 1 of the assignment.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    nrow = maze.rows 
    ncol = maze.cols 
    visited = [[0 for i in range(ncol)] for i in range(nrow)] 

    parent_list = {start_point : None}
    distance_list = {start_point : 0}

    q = PriorityQueue.Q_for_maze_single(maze, distance_list, goal)
    q.insert(start_point)
    
    not_arrived = True
    while not_arrived:
        # find most prior one and switch it to closed list. 
        # mark it as visited 
        next_step = q.pop()
        
        for next_pos in maze.getNeighbors(next_step[0], next_step[1]): 
            if maze.isValidMove(next_pos[0], next_pos[1]) and visited[next_pos[0]][next_pos[1]] == 0:
                parent_list[next_pos] = next_step 
                distance_list[next_pos] = distance_list[next_step] + 1 
                visited[next_pos[0]][next_pos[1]] = 1 
                q.insert(next_pos)
            
            if next_pos == goal:
                not_arrived = False 
                break
        
    node = goal
    path = []
    while parent_list[node] != start_point:
        path.insert(0, node)
        node = parent_list[node]
    path.insert(0,node)
    path.insert(0, start_point)
    
    return path, len(path)
            
            
            
           
 


def astar_multi(maze):
    """
    Runs A star for part 2 of the assignment in the case where there are
    multiple objectives.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here
    goals = maze.getObjectives() 
    start_point = maze.getStart()
    points = [start_point] + goals 
    name_dic = {}
    for i, point in enumerate(points):
        name_dic[i] = point 

    dist_dic = {}
    path_dic = {} 
    for i in range(len(points)):
        for j in range(i, len(points)):
            start = points[i]
            end = points[j]
            path, length = astar_helper(maze, start, end)
            path_dic[(i, j)] = path 
            path_dic[(j, i)] = path[::-1]
            dist_dic[(i, j)] = length 
            dist_dic[(j, i)] = length

    

    


def extra(maze):
    """
    Runs extra credit suggestion.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here
    return []

