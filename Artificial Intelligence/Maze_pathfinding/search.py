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

class DisjointSet(object):
    def __init__(self, array):
        self.array = array
        self.roots = [-1] * len(array)
    
    def find_root(self, index):
        if self.roots[index] < 0:
            return index
        else:
            current_root = self.find_root(self.roots[index])
            self.roots[index] = current_root 
            return current_root


    def set_union(self, index1 , index2):
        root1 = self.find_root(index1)
        root2 = self.find_root(index2)
        if root1 == root2 and root1 and (root1 != -1 or root2 != -1):
            return 
            
        size = self.roots[root1] + self.roots[root2]
        if abs(self.roots[root1]) >= abs(self.roots[root2]):
            self.roots[root2] = root1
            self.roots[root1] = size
        else:
            self.roots[root1] = root2
            self.roots[root2] = size



class PriorityQueue(object): ### min first
    def __init__(self):
        self.heap = [-1]
        
    def pop(self): ### remove the most prior one
        if len(self.heap) == 1:
            return
        temp = self.heap[-1]
        prior = self.heap[1]
        self.heap[-1] = self.heap[1]
        self.heap[1] = temp
        self.heap.pop(-1)
        self.heapify_down(1)
        return prior

    def insert(self, node):
        self.heap.append(node) 
        self.heapify_up(len(self.heap) - 1)

    def heapify_up(self, index):
        if (index // 2 == 0):
            return 
        swap = self.calculate_priority(self.parent(index)) >= self.calculate_priority(self.heap[index])

        if swap:
            temp = self.parent(index)
            self.heap[index // 2] = self.heap[index]
            self.heap[index] = temp 
            self.heapify_up(index // 2)
        
        
    def heapify_down(self, index):
        if(2 * index + 1 >= len(self.heap)):
            return 

        left = self.calculate_priority(self.left_child(index)) <= self.calculate_priority(self.right_child(index))
        min_child = self.left_child(index) if left else self.right_child(index)
        min_index = 2 * index if left else 2 * index + 1
        swap = self.calculate_priority(min_child) <= self.calculate_priority(self.heap[index])

        if swap:
            self.heap[min_index] = self.heap[index]
            self.heap[index] = min_child
            self.heapify_down(min_index)

            
    def parent(self, index):
        return self.heap[index // 2]

    def left_child(self, index):
        return self.heap[2 * index]
    
    def right_child(self, index):
        return self.heap[2 * index + 1]

    def calculate_priority(self, node):
        return node



class Q_for_maze_single(PriorityQueue):
    def __init__(self, maze, distance_list, goal):
        self.heap = [-1]
        self.maze = maze
        self.goal = goal
        self.distance_list = distance_list
    

    def calculate_priority(self, node):
        return self.distance_list[node] + abs(self.goal[0] - node[0]) + abs(self.goal[1] - node[1])


class Q_for_maze_multi(PriorityQueue):
    def __init__(self, maze, distance_list, goals_status, mst_len):
        self.heap = [-1]
        self.maze = maze
        self.distance_list = distance_list
        self.goals_status = goals_status
        self.mst_len = mst_len
    

    def calculate_priority(self, node):
        dist, next_goal = self.find_nearest_goal(node, [goal for goal in self.goals_status.keys() if self.goals_status[goal] == False])
        return self.distance_list[node] + dist + self.mst_len[0]

    def find_nearest_goal(self, node, nexts):
        min_dist = 999999999999
        next_goal = None
        for temp in nexts: 
            dist = abs(node[0] - temp[0]) + abs(node[1] - temp[1])
            change = dist < min_dist
            min_dist = dist if change else min_dist
            next_goal = temp if change else next_goal 
        return min_dist, next_goal


def search(maze, searchMethod):
    return {
        "bfs": bfs,
        "dfs": dfs,
        "astar": astar,
        "astar_multi": astar_multi,
        "extra": extra,
    }.get(searchMethod)(maze)





def bfs(maze):
    """
    Runs BFS for part 1 of the assignment.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here
    # print("this is the BFS method")

    nrow = maze.rows 
    ncol = maze.cols 
    visited = [[0 for i in range(ncol)] for i in range(nrow)] 
    

    start_point = maze.getStart() ## this is a tuple
    queue = [[start_point]]
    goal = maze.getObjectives()[0]  ## this is a list
    while queue:
        current_pos = queue[0][-1]
        current_path = queue[0]
        queue.pop(0)

        for next_position in maze.getNeighbors(current_pos[0], current_pos[1]):

            next_x = next_position[0]
            next_y = next_position[1]

            if next_position == goal:
                return current_path + [goal]
                

            if maze.isValidMove(next_x, next_y) and visited[next_x][next_y] == 0:
                visited[next_x][next_y] = 1
                queue.append(current_path + [next_position]) 

    return queue[-1]


def print_visited(visited):
    for l in visited:
        print(l)
    print("==========================")


# def dfs(maze):
#     """
#     Runs DFS for part 1 of the assignment.

#     @param maze: The maze to execute the search on.

#     @return path: a list of tuples containing the coordinates of each state in the computed path
#     """
#     # TODO: Write your code here
    
#     print("this is the DFS method")
    
    
#     start_point = maze.getStart() ## this is a tuple
#     # stack = [start_point]
#     goal = maze.getObjectives()[0]  
#     nrow = maze.rows 
#     ncol = maze.cols 
#     visited = [[0 for i in range(ncol)] for i in range(nrow)] 
#     stack = [start_point]
    
#     while True:
#         movable = False
#         current_pos = stack[-1]
#         visited[current_pos[0]][current_pos[1]] = 1
#         neighbors = maze.getNeighbors(current_pos[0], current_pos[1])
#         shuffled = neighbors[::-1]
#         for next_pos in shuffled:

#             if next_pos == goal:
#                 return stack + [goal]

            
#             next_x = next_pos[0]
#             next_y = next_pos[1]
#             if maze.isValidMove(next_x, next_y) and visited[next_x][next_y] == 0:
#                 movable = True
#                 # visited[next_x][next_y] = 1
#                 stack.append(next_pos) 
#                 break
#                 # print(stack)

#         if not movable:
#             stack.pop(-1)

        
def dfs(maze):
    """
    Runs DFS for part 1 of the assignment.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here
    nrow = maze.rows 
    ncol = maze.cols
    start_point = maze.getStart()
    path = [start_point]
    goal = maze.getObjectives()[0]
    visited = [[0 for i in range(ncol)] for i in range(nrow)]
    stack = [(start_point, path)]
    while stack:
        current_pos, path = stack.pop()
        visited[current_pos[0]][current_pos[1]] = 1
        if current_pos == goal:
            return path

        for next_pos in maze.getNeighbors(current_pos[0], current_pos[1]):
            if maze.isValidMove(next_pos[0], next_pos[1]) and visited[next_pos[0]][next_pos[1]] == 0:
                stack.append((next_pos, path + [next_pos]))









    

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
    return astar_helper(maze, maze.getStart(), maze.getObjectives()[0])[0]

        
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

    q = Q_for_maze_single(maze, distance_list, goal)
    q.insert(start_point)
    
    not_arrived = True
    while not_arrived:
        # find most prior one and switch it to closed list. 
        # mark it as visited 
        next_step = q.pop()
        
        for next_pos in maze.getNeighbors(next_step[0], next_step[1]): 
            if maze.isValidMove(next_pos[0], next_pos[1]) and visited[next_pos[0]][next_pos[1]] == 1:
                if distance_list[next_step] + 1 < distance_list[next_pos]:
                    parent_list[next_pos] = next_step
                    distance_list[next_pos] = distance_list[next_step] + 1
                    continue

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
            
            
            

#############################################
class State(object):
    def __init__(self, path, num_to_point, point_to_num, dist_dic):
        self.path = path  ##### path contains the number of points e.g: [0, 1, 3, 6]
        self.to_be_visited = []   ## e.g:[5,7,8,9]
        self.dist_dic = dist_dic
        for point in num_to_point.keys(): 
            flag = point in path       
            if not flag:
                self.to_be_visited.append(point)

############################################
class Q_states(PriorityQueue):
    def __init__(self):
        self.heap = [-1]
    
        
    def calculate_priority(self, state):
        cost_from_start = 0
        for i in range(len(state.path) - 1):
            cost_from_start += state.dist_dic[(state.path[i], state.path[i + 1])] 
        mst_cost = construct_mst(state.to_be_visited, state.dist_dic)
        return mst_cost + cost_from_start 



###################################
def construct_astar_distance(maze):
    goals = maze.getObjectives() 
    start_point = maze.getStart()
    points = [start_point] + goals 
    num_to_point = {}
    point_to_num = {}
    for i, point in enumerate(points):
        num_to_point[i] = point 
        point_to_num[point] = i  

    dist_dic = {}
    path_dic = {} 
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            start = points[i]
            end = points[j]
            path, length = astar_helper(maze, start, end)
            path_dic[(i, j)] = path 
            path_dic[(j, i)] = path[::-1]
            dist_dic[(i, j)] = length          
            dist_dic[(j, i)] = length
    return num_to_point, point_to_num, dist_dic, path_dic 

# def construct_manh_distance(maze, goals_status):
#     points = [goal for goal in goals_status.keys() if goals_status[goal] == False] 
#     num_to_point = {}
#     for i, point in enumerate(points):
#         num_to_point[i] = point 

#     dist_dic = {}
#     for i in range(len(points)):
#         for j in range(i + 1, len(points)):
#             start = points[i]
#             end = points[j]
#             dist = abs(start[0] - end[0]) - abs(start[1] - end[1])
#             dist_dic[(i, j)] = dist 
#     return num_to_point, dist_dic 


def construct_mst(to_be_visited, dist_dic):
    ### would return the total length of the mst!!!
    dset = DisjointSet(to_be_visited)
    ordered_edge = []
    mst_len = 0
    edge_weight_dic = {}
    point_to_idx = {n : i for n,i in zip(to_be_visited, range(len(to_be_visited)))} 
    
    for i in range(len(to_be_visited)):
        for j in range(i + 1, len(to_be_visited)):
            edge_weight_dic[(to_be_visited[i],to_be_visited[j])] = dist_dic[(to_be_visited[i], to_be_visited[j])]

    for key, value in sorted(edge_weight_dic.items(), key = lambda item : item[1]):
        ordered_edge.append(key)


    for start_end in ordered_edge:  
        if dset.find_root(point_to_idx[start_end[0]]) != dset.find_root(point_to_idx[start_end[1]]):
            dset.set_union(point_to_idx[start_end[0]], point_to_idx[start_end[1]])
            mst_len += dist_dic[start_end]
            
    return mst_len 





def astar_multi(maze):
    """
    Runs A star for part 2 of the assignment in the case where there are
    multiple objectives.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here
    num_to_point, point_to_num, dist_dic, path_dic = construct_astar_distance(maze)
    len_goals = len(maze.getObjectives())
    # visited = [[0 for i in range(ncol)] for i in range(nrow)]
    ini_state = State([point_to_num[maze.getStart()]], num_to_point, point_to_num, dist_dic)
    Q = Q_states()
    Q.insert(ini_state)

    
    while True:
        finished = False 
        current_state = Q.pop()
        next_points = current_state.to_be_visited

        for next_pos in next_points:
            path = current_state.path + [next_pos]
            next_state = State(path, num_to_point, point_to_num, dist_dic)
            Q.insert(next_state)
            if len(next_state.path) - 1 == len_goals:
                finished = True 
                break  
        if finished:
            break 
    
    final_path = []
    for i in range(len(next_state.path) - 1):
        pre, post = next_state.path[i], next_state.path[i + 1]
        temp_path = path_dic[(pre, post)]
        final_path = final_path + temp_path[:-1]
        if i == len(next_state.path) - 2:
            final_path = final_path + [temp_path[-1]]
    
    return final_path


    ################## Manhattan approach
    # goals_status = {goal : False for goal in goals}
    # start_point = maze.getStart()
    # parent_list = {}
    # distance_list = {start_point : 0}
    # a,b = construct_manh_distance(maze, goals_status)
    # current_mst_len = [construct_mst(a,b)]
    # Q = Q_for_maze_multi(maze, distance_list, goals_status, current_mst_len)
    # Q.insert(start_point) 
    # path = []

    # while True:
    #     current_pos = Q.pop()
    #     finished = False
    #     for next_pos in maze.getNeighbors(current_pos[0], current_pos[1]):

    #         # if maze.isValidMove(next_pos[0], next_pos[1]) and visited[next_pos[0]][next_pos[1]] == 1:
    #         #     if distance_list[current_pos] + 1 < distance_list[next_pos]: 
    #         #         distance_list[next_pos] = distance_list[current_pos] + 1
    #         #         parent_list[next_pos] = current_pos 
    #         #         continue 

    #         if maze.isValidMove(next_pos[0], next_pos[1]) and visited[next_pos[0]][next_pos[1]] == 0:
    #             distance_list[next_pos] = distance_list[current_pos] + 1
    #             parent_list[next_pos] = current_pos 
    #             visited[next_pos[0]][next_pos[1]] = 1
    #             Q.insert(next_pos)
    #             path.append(next_pos)

    #         if next_pos in goals_status.keys() and not goals_status[next_pos]:
    #             print("arrived")
    #             goals_status[next_pos] = True
    #             total_visited += 1 
    #             node = next_pos 
    #             while parent_list[node] != start_point:
    #                 path.insert(0, node)
    #                 node = parent_list[node]
    #             path.insert(0,node)
    #             path.insert(0, start_point)   
    #             return path

    #             start_point = next_pos
    #             for point in path:
    #                 visited[point[0]][point[1]] = 0

    #             if total_visited == len(goals):
    #                 finished = True
    #                 break
    #             a,b = construct_manh_distance(maze, goals_status)
    #             current_mst_len = [construct_mst(a,b)]

    #     if finished:
    #         break   
    
    # # node = next_pos
    # # path = []
    # # while parent_list[node] != start_point:
    # #     path.insert(0, node)
    # #     node = parent_list[node]
    # # path.insert(0,node)
    # # path.insert(0, start_point)        
    # # print(path)
    # return path

        
def heuristic_extra(current_pos, goals, distance):
    s = 0
    for goal in goals:
        s += abs(current_pos[0] - goal[0]) + abs(current_pos[1] - goal[1]) 
    return s + distance


import heapq as hq
def extra(maze):
    """
    Runs extra credit suggestion.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here
    nrow = maze.rows 
    ncol = maze.cols 
    start_point = maze.getStart()
    path = [start_point]
    goals = maze.getObjectives()
    visited = [[0 for i in range(ncol)] for i in range(nrow)]
    Q = []
    distance = 0
    hq.heappush(Q, (heuristic_extra(start_point, goals, distance), start_point, path))
    
    while True:
        current_cost, current_pos, path  = hq.heappop(Q)
        visited[current_pos[0]][current_pos[1]] = 1
            
        if current_pos in goals:
            goals.remove(current_pos)
            if len(goals) == 0:
                return path
            start_point = current_pos
            Q = []
            distance = 0
            visited = [[0 for i in range(ncol)] for i in range(nrow)]
            hq.heappush(Q, (heuristic_extra(start_point, goals, distance), start_point, path))
            continue

        for next_pos in maze.getNeighbors(current_pos[0], current_pos[1]):
            if maze.isValidMove(next_pos[0], next_pos[1]) and visited[next_pos[0]][next_pos[1]] == 0:
                distance += 1
                hq.heappush(Q, (heuristic_extra(start_point, goals, distance), next_pos, path + [next_pos]))