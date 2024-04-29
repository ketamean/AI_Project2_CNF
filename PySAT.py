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
# -------------Implementation-----------------
# DNF from board, for all '_' cells, generate clauses for each possibility (trap or gem)
# For each empty cell (contain a number), enforce that the number of neighboring traps matches the number indicated in the cell. (in 8 directions)


class PySatSolver:
    def __init__(self, clauses: list):
        cnf = CNF(from_clauses=clauses)
        self.solver = self.solver = Solver(name='g3', bootstrap_with=cnf)

    def solve(self) -> list | None:
        result = self.solver.solve()  # Solve the CNF formula
        if result:
            return self.solver.get_model()
        return None
