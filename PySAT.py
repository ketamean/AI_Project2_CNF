from pysat.solvers import Solver
from pysat.formula import CNF

# -------------Documentation-----------------
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
# -------------Justification-----------------
"""
The implementation uses the PySAT library to encode the variables and constraints of the Gem Hunter puzzle as a CNF formula.
It then uses a SAT solver to find a satisfying assignment that represents the solution to the puzzle.
The implementation is efficient and scalable, as it can handle grids of any size and solve the puzzle in a reasonable amount of time.
The use of a SAT solver ensures that the solution is correct and optimal, as it guarantees that all constraints are satisfied.
"""
# -------------Implementation of clauses generation-----------------
# DNF from board, for all '_' cells, generate clauses for each possibility (trap or gem)
# For each empty cell (contain a number), enforce that the number of neighboring traps matches the number indicated in the cell. (in 8 directions)

# How this works:
# The cells on the board are numbered from 1 to n*m. (representing the variables in the CNF formula: x1, x2, x3, ...)
# For each cell, we generate a list of clauses that represent the possible configurations of traps around that cell.
# Ex: If N_ij = 2, then there are 2 traps around the cell (i, j).
# The number of sub_clauses = 8C(8-Nij+1) + 8C(Nij+1) = 8C7 + 8C3 = 8 + 56 = 64
# NOTICE: THERE ARE BORDER CASES THAT NEED TO BE HANDLED (Ex: for the pos (0, 0), we only have 3 neighbors, not 8)
# Ex: If (i,j) = (0,0) (AKA cell No.1) and N_ij = 1. The sub_clauses would be: [[2, 5], [2, 6], [5, 6], [-2, -5, -6]]
# To handle this, we need to check if the neighbor is within the grid bounds before adding it to the sub_clauses.
# SOLUTION: added the m, n parameters to check if the neighbor is within the grid bounds.    

# Actual Math format of a Nij = 2, i = 0, j = 0 (cell No.1) would be: 
# sub_clauses amount = 3C(3-2+1) + 3C(2+1) = 3C2 + 3C3 = 3 + 1 = 4
# (x2 v x5) ^ (x2 v x6) ^ (x5 v x6) ^ (-x2 v -x5 v -x6)

class PySatSolver:
    def __init__(self, clauses: list, solver: str):
        cnf = CNF(from_clauses=clauses)
        self.solver = Solver(name=solver, bootstrap_with=cnf) # Initialize the solver with the CNF formula

    def solve(self) -> list | None:
        result = self.solver.solve()  # Solve the CNF formula
        if result:
            return self.solver.get_model() # Return the satisfying assignment if a solution is found
        return None
