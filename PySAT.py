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
from pysat.solvers import Solver
from pysat.formula import CNF
import copy

# from CDCL import Solver

# DNF from board, for all '_' cells, generate clauses for each possibility (trap or gem)
# For each empty cell (contain a number), enforce that the number of neighboring traps matches the number indicated in the cell. (in 8 directions)


class BoardCNF:
    def __init__(self, board: list, n: int, m: int):
        self.main_board = []
        for row in board:
            m_row = []
            for item in row:
                if '0' <= item <= '9':
                    m_row.append(int(item))
                else:
                    m_row.append(item)
            self.main_board.append(m_row)
        self.n = n
        self.m = m
        self.id_board = t = [[0] * m for i in range(n)]
        self.result_clauses = []
        for i in range(0, n):
            for j in range(0, m):
                self.id_board[i][j] = i * m + j + 1

    def update_board(self, board: list):
        """ Update current main board to a new board."""

        self.main_board = copy.deepcopy(board)
        self.result_clauses = self.gen_clauses()

    @staticmethod
    def gen_combine(num_trap_cells: int, pos_trap_cells: list) -> list:
        import itertools
        greater_equal = list(itertools.combinations(pos_trap_cells, len(pos_trap_cells) - num_trap_cells + 1))
        lower_equal = list(itertools.combinations(pos_trap_cells, num_trap_cells + 1))
        combinations_clause = []
        for item in greater_equal:
            combinations_clause.append(list(item))
        for item in lower_equal:
            neg_item = []
            for i in list(item):
                neg_item.append(-1 * i)
            combinations_clause.append(neg_item)
        return combinations_clause

    def add_cells_clauses(self, row: int, col: int) -> None:
        # print(row, col)
        pos_trap_cells = []
        num_trap_cells = self.main_board[row][col]
        for delta_row in range(-1, 2):
            for delta_col in range(-1, 2):
                x = row + delta_row
                y = col + delta_col
                if 0 <= x < self.n and 0 <= y < self.m:
                    if self.main_board[x][y] == '_':
                        pos_trap_cells.append(self.id_board[x][y])
                    elif self.main_board[x][y] == 'T':
                        num_trap_cells -= 1
        clauses = self.gen_combine(num_trap_cells, pos_trap_cells)

        for clause in clauses:
            self.result_clauses.append(clause)

    def gen_clauses(self) -> list:
        """Gen clauses using current main board and return a list that contains all the clauses."""
        self.result_clauses.clear()
        for i in range(0, self.n):
            for j in range(0, self.m):
                if type(self.main_board[i][j]) is int:
                    self.add_cells_clauses(i, j)
        return self.result_clauses


class GemHunter:
    def __init__(self):
        self.board = []
        self.n = 0  # Number of rows
        self.m = 0  # Number of columns
        self.solver = Solver()

    def gen_board(self, filepath):
        with open(filepath, 'r') as f:
            lines = f.readlines()
            for line in lines:
                row = line.strip().split(', ')
                self.board.append(row)
                self.n += 1  # Number of rows
                self.m = len(row)  # Number of columns

        # Print the board
        # print('Input:')
        # for row in self.board:
        #     print(','.join(row))
        # print()

    def solve(self, solver):
        board_cnf = BoardCNF(self.board, self.n, self.m)
        clause = board_cnf.gen_clauses()
        #print('Clauses:', clause)
        cnf = CNF(from_clauses=clause)
        self.solver = Solver(name=solver, bootstrap_with=cnf)
        result = self.solver.solve()  # Solve the CNF formula
        if result:
            model = self.solver.get_model()
            #print('Model:', model)
            solution = copy.deepcopy(self.board)
            for i in range(self.n):
                for j in range(self.m):
                    if solution[i][j] == '_':
                        if model[(i * self.m + j)] > 0:  # (i * self.m + j) + 1 is the index of the variable in the model
                            solution[i][j] = 'T'
                        else:
                            solution[i][j] = 'G'
            return solution
        else:
            return None


# -------------Example-----------------
if __name__ == '__main__':
    gem_hunter = GemHunter()
    gem_hunter.gen_board('testcases/trivial.txt')
    result = gem_hunter.solve('g3')  # Others: 'g4', Cadical(), etc.
    if result:
        print('Solution:')
        for row in result:
            print(','.join(row))
    else:
        print('No solution found.')
