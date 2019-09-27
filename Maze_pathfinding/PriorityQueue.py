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
