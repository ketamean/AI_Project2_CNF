import cdcl
from BoardCNF import BoardCNF
import PySAT
import copy

class GemHunter:
    def __init__(self):
        self.board = []
        self.n = 0  # Number of rows
        self.m = 0  # Number of columns
        self.res_board = None

    def gen_board(self, filepath):
        self.res_board = None
        with open(filepath, 'r') as f:
            lines = f.readlines()
            for line in lines:
                row = line.strip().split(', ')
                self.board.append(row)
                self.n += 1  # Number of rows
                self.m = len(row)  # Number of columns

    def create_board_result(self, result_list):
        self.res_board = copy.deepcopy(self.board)
        for i in range(self.n):
            for j in range(self.m):
                if self.res_board[i][j] == '_':
                    if result_list[(i * self.m + j)] > 0:  # (i * self.m + j) + 1 is the index of the variable in the model
                        self.res_board[i][j] = 'T'
                    else:
                        self.res_board[i][j] = 'G'

    def solve(self, solve_id: int):
        board_cnf = BoardCNF(self.board, self.n, self.m)
        clauses = board_cnf.gen_clauses()
        if solve_id == 1:
            pysat_solver = PySAT.PySatSolver(clauses)
            pysat_res = pysat_solver.solve()
            if pysat_res:
                self.create_board_result(pysat_res)
        elif solve_id == 2:
            cdcl_solver = cdcl.Solver(clauses)
            cdcl_res = cdcl_solver.solve()
            if cdcl_res:
                self.create_board_result(cdcl_res)
        elif solve_id == 3:
            pass
        elif solve_id == 4:
            pass


if __name__ == '__main__':
    gem_hunter = GemHunter()
    gem_hunter.gen_board('testcases/test4.txt')
    print("Please choose an algorithms, enter a number")
    print("1. PySAT")
    print("2. CDCL (self implementation)")
    print("3. Backtracking algorithm")
    print("4. Brute-force algorithm")
    x = int(input())
    gem_hunter.solve(x)
    result = gem_hunter.res_board
    if result:
        print('Solution:')
        for row in result:
            print(','.join(row))
    else:
        print('No solution found.')
