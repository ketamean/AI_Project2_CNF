#-------------Documentation----------------- 
"""
Using the pysat library to find the value for each variable and infer the result.
    You are asked to build a gem hunter game by using CNF as described below:
    Gem Hunter is a strategic puzzle game where players explore a grid to reveal valuable gems while avoiding dangerous
    traps. The objective is to reveal all the gems on the grid without triggering any traps. Players must use logic and
    deduction to strategically uncover tiles and mark potential trap locations. You will know the location of the trap
    through the tiles on the map. Each number on a tile represents the number of traps around that tile.

    The rules are as follows:
    • The grid has a dimension of n x m.
    • Each empty cell (only number) contains a number that represents the number of traps around that cell.
    • An unkown cell is represented by the symbol _ (can be T or G).
    • A cell can have at most 8 neighbors. (up, down, left, right, and diagonal)
    • The objective is to determine the location of the traps and the gems.
    • A trap is represented by the symbol T.
    • A gem is represented by the symbol G.
"""
""" 
File format: 
Input:
3, _, 2, _
_, _, 2, _
_, 3, 1, _

Output:
3, T, 2, G
T, T, 2, G
T, 3, 1, G 
"""
#-------------Justification-----------------
"""
The implementation uses the PySAT library to encode the variables and constraints of the Gem Hunter puzzle as a CNF formula.
It then uses a SAT solver to find a satisfying assignment that represents the solution to the puzzle.
The implementation is efficient and scalable, as it can handle grids of any size and solve the puzzle in a reasonable amount of time.
The use of a SAT solver ensures that the solution is correct and optimal, as it guarantees that all constraints are satisfied.
"""
#-------------Implementation-----------------
from pysat.solvers import Solver
from pysat.formula import CNF
import copy
# DNF from board, for all '_' cells, generate clauses for each possibility (trap or gem)
# For each empty cell (contain a number), enforce that the number of neighboring traps matches the number indicated in the cell. (in 8 directions)


class GemHunter:
    def __init__(self):
        self.board = []
        self.n = 0 # Number of rows
        self.m = 0 # Number of columns
        self.solver = Solver() 
        
    def gen_board(self, filepath):
        with open(filepath, 'r') as f:
            lines = f.readlines()
            for line in lines:
                row = line.strip().split(', ') 
                self.board.append(row)
                self.n += 1 # Number of rows
                self.m = len(row) # Number of columns
                
        # Print the board
        print('Input:')        
        for row in self.board:
            print(','.join(row))
        print()
            

    def solve(self, solver):
        clause = gen_clauses(self.board, self.n, self.m)
        print('Clauses:', clause)
        cnf = CNF(from_clauses=clause)
        self.solver = Solver(name=solver, bootstrap_with=cnf) 
        result = self.solver.solve() # Solve the CNF formula 
        if result:
            model = self.solver.get_model() 
            print('Model:', model)
            solution = copy.deepcopy(self.board)
            for i in range(self.n):
                for j in range(self.m):
                    if solution[i][j] == '_':
                        if model[(i * self.m + j) + 1] > 0: # (i * self.m + j) + 1 is the index of the variable in the model
                            solution[i][j] = 'T'
                        else:
                            solution[i][j] = 'G'
            return solution
        else:
            return None
                        
        
#-------------Example-----------------
if __name__ == '__main__':
    gem_hunter = GemHunter()
    gem_hunter.gen_board('test1.txt')
    result = gem_hunter.solve('g3') # Others: 'g4', Cadical(), etc.
    if result:
        print('Solution:')
        for row in result:
            print(','.join(row))
    else:
        print('No solution found.')
    
    
        
        
        