import cdcl
from BoardCNF import BoardCNF
import PySAT
import BruteForce_Backtrack
import copy # For deep copy of the board to store the result of the solution

# -------------Documentation-----------------
"""
The GemHunter class is responsible for reading the input file, generating the board, and solving the puzzle using different methods.
The gen_board method reads the input file and generates the board.
The create_board_result method creates a new board with the solution based on the result list.
The solve method takes a solve_id as input and calls the corresponding solver method based on the id.
The main method reads the input file, generates the board, and prompts the user to choose a solving method.
**Note: THE BOARD ALLOWS FOR A RECTANGULAR SHAPE, NOT JUST SQUARE.
"""

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
                row = line.strip().split(', ') # Split the row by ', '
                self.board.append(row)
                self.n += 1  # Number of rows
                self.m = len(row)  # Number of columns

    def create_board_result(self, result_list):
        self.res_board = copy.deepcopy(self.board)
        for i in range(self.n):
            for j in range(self.m):
                if self.res_board[i][j] == '_':
                    if result_list[(i * self.m + j)] > 0:  # (i * self.m + j) is the index of the variable in the model
                        self.res_board[i][j] = 'T' 
                    else:
                        self.res_board[i][j] = 'G'

    def solve(self, solve_id: int, input_file: str):
        board_cnf = BoardCNF(self.board, self.n, self.m)
        #print('Input:')
        #print('\n'.join([', '.join(row) for row in self.board]))
        clauses = board_cnf.gen_clauses()
        if solve_id == 1:
            solver_name = input('Please enter the name of a PySAT solver (g4, g3, m22, etc): ')
            pysat_solver = PySAT.PySatSolver(clauses, solver_name)
            pysat_res = pysat_solver.solve()
            if pysat_res:
                self.create_board_result(pysat_res)
        elif solve_id == 2:
            cdcl_solver = cdcl.Solver(clauses)
            cdcl_res = cdcl_solver.solve()
            if cdcl_res:
                self.create_board_result(cdcl_res)
        if solve_id == 3:
            # print('Using Backtracking:')
            backtracking = BruteForce_Backtrack.Backtracking()
            solution = backtracking.run(input_file)
            if solution:
                self.res_board = solution
        elif solve_id == 4:
            # print('Using Brute Force:')
            brute_force = BruteForce_Backtrack.BruteForce()
            solution = brute_force.run(input_file)
            if solution:
                self.res_board = solution


if __name__ == '__main__':
    print('-----------------Gem Hunter-----------------')
    gem_hunter = GemHunter()
    input_file = input('Enter the input file path: ')
    gem_hunter.gen_board(input_file)
    print('Solver options:')
    print("1. PySAT")
    print("2. CDCL (self implementation)")
    print("3. Backtracking algorithm")
    print("4. Brute-force algorithm")
    solver = int(input('Please choose a solving method (1-4): '))
    gem_hunter.solve(solver, input_file)
    result = gem_hunter.res_board
    if result:
        print('\nSolution:')
        for row in result:
            print(', '.join(row))
    else:
        print('\nNo solution found.')
