import os
import sys
import copy

visited_nodes = set()
result = list()
get_empty_cell_new_puzzle = 0
class Puzzle(object):
    def __init__(self, init_state, goal_state):
        # you may add more attributes if you think is useful
        self.size = len(init_state) 
        self.init_state = init_state
        self.goal_state = goal_state
        self.actions = list()
        self.empty_cell_position = [-1, -1]

    def getEmptyCellPosition(self):
        if self.empty_cell_position != [-1, -1]:
            return self.empty_cell_position
        for i in range(0, self.size):
            for j in range(0, self.size):
                cell_value = self.init_state[i][j]
                if cell_value == 0:
                    return [i, j]

   
    def moveEmptyCellToLeft(self):
        empty_cell_position = self.getEmptyCellPosition()
        new_puzzle = copy.deepcopy(self)
        new_state = new_puzzle.init_state
        row = empty_cell_position[0]
        col = empty_cell_position[1]
        if col <= 0:
            return Puzzle([], [])
        else:
            new_state[row][col] = new_state[row][col - 1]
            new_state[row][col - 1] = 0
        new_puzzle.empty_cell_position = [row, col - 1]
        new_puzzle.actions.append("RIGHT")
        return new_puzzle

    def moveEmptyCellUp(self):
        empty_cell_position = self.getEmptyCellPosition()
        new_puzzle = copy.deepcopy(self)
        new_state = new_puzzle.init_state
        row = empty_cell_position[0]
        col = empty_cell_position[1]
        if row <= 0:
            return Puzzle([], []) 
        else:
            new_state[row][col] = new_state[row - 1][col]
            new_state[row - 1][col] = 0
        new_puzzle.actions.append("DOWN")
        new_puzzle.empty_cell_position = [row - 1, col]
        return new_puzzle
        

    def moveEmptyCellToRight(self):
        empty_cell_position = self.getEmptyCellPosition()
        new_puzzle = copy.deepcopy(self)
        new_state = new_puzzle.init_state
        row = empty_cell_position[0]
        col = empty_cell_position[1]
        if col >= self.size - 1:
            return Puzzle([], []) 
        else:
            new_state[row][col] = new_state[row][col + 1]
            new_state[row][col + 1] = 0
        new_puzzle.actions.append("LEFT")
        new_puzzle.empty_cell_position = [row, col + 1]
        return new_puzzle

    def moveEmptyCellDown(self):
        empty_cell_position = self.getEmptyCellPosition()
        new_puzzle = copy.deepcopy(self)
        new_state = new_puzzle.init_state
        row = empty_cell_position[0]
        col = empty_cell_position[1]
        if row >= self.size - 1:
            return Puzzle([], []) 
        else:
            new_state[row][col] = new_state[row + 1][col]
            new_state[row + 1][col] = 0
        new_puzzle.empty_cell_position = [row + 1, col]
        new_puzzle.actions.append("UP")
        return new_puzzle

    def DLS(self, depth, limit):
        global result
        # puzzle state is invalid
        if self.init_state == []:
            return False 
        if self.init_state == self.goal_state:
            result = self.actions
            return True
        if depth > limit:
            return False
        # checks if node has been visited before    
        tuple_for_set = tuple(map(tuple, self.init_state))
        if tuple_for_set in visited_nodes:
            return False
        visited_nodes.add(tuple_for_set)
            

        return self.moveEmptyCellToRight().DLS(depth + 1, limit) or self.moveEmptyCellToLeft().DLS(depth + 1, limit) or \
            self.moveEmptyCellUp().DLS(depth + 1, limit) or self.moveEmptyCellDown().DLS(depth + 1, limit)


    def solve(self):
        global visited_nodes
        for limit in range(0, 50):
            visited_nodes = set()
            if self.DLS(0, limit):
                print(result)
                return result

        print("UNSOLVABLE")
        return ["UNSOLVABLE"]
        

    # you may add more functions if you think is useful

if __name__ == "__main__":
    # do NOT modify below

    # argv[0] represents the name of the file that is being executed
    # argv[1] represents name of input file
    # argv[2] represents name of destination output file
    if len(sys.argv) != 3:
        raise ValueError("Wrong number of arguments!")

    try:
        f = open(sys.argv[1], 'r')
    except IOError:
        raise IOError("Input file not found!")

    lines = f.readlines()
    
    # n = num rows in input file
    n = len(lines)
    # max_num = 2 to the power of n - 1
    max_num = n ** 2 - 1

    # Instantiate a 2D list of size n x n
    init_state = [[0 for i in range(n)] for j in range(n)]
    goal_state = [[0 for i in range(n)] for j in range(n)]
    

    i,j = 0, 0
    for line in lines:
        for number in line:
            if '0'<= number <= str(max_num):
                init_state[i][j] = int(number)
                j += 1
                if j == n: #??
                    i += 1
                    j = 0

    for i in range(1, max_num + 1):
        goal_state[(i-1)//n][(i-1)%n] = i
    goal_state[n - 1][n - 1] = 0

    puzzle = Puzzle(init_state, goal_state)
    ans = puzzle.solve()

    with open(sys.argv[2], 'a') as f:
        for answer in ans:
            f.write(answer+'\n')







