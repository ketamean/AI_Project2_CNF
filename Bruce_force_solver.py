import itertools
from typing import List, Tuple
import time

class BruteForceGemHunter:
    def __init__(self):
        self.board = []
        self.n = 0  # Number of rows
        self.m = 0  # Number of columns

    def gen_board(self, filepath):
        with open(filepath, 'r') as f:
            lines = f.readlines()
            for line in lines:
                row = line.strip().split(', ')
                self.board.append(row)
                self.n += 1  # Number of rows
                self.m = len(row)  # Number of columns

        # Print the board
        print('Input:')
        for row in self.board:
            print(','.join(row))
        print()

    def is_valid_solution(self, solution):
        for i in range(self.n):
            for j in range(self.m):
                if self.board[i][j].isdigit():
                    count = 0
                    for di, dj in itertools.product([-1, 0, 1], repeat=2):
                        if di == dj == 0:
                            continue
                        ni, nj = i + di, j + dj
                        if 0 <= ni < self.n and 0 <= nj < self.m and solution[ni][nj] == 'T':
                            count += 1
                    if count != int(self.board[i][j]):
                        return False
        return True

    def brute_force_solve(self):
        start_time = time.time()
        for trap_gems in itertools.product(['T', 'G'], repeat=sum(cell == '_' for row in self.board for cell in row)):
            solution = [['_' for _ in range(self.m)] for _ in range(self.n)]
            trap_gem_index = 0
            for i in range(self.n):
                for j in range(self.m):
                    if self.board[i][j] == '_':
                        solution[i][j] = trap_gems[trap_gem_index]
                        trap_gem_index += 1
                    else:
                        solution[i][j] = self.board[i][j]

            if self.is_valid_solution(solution):
                end_time = time.time()
                print('Solution found in {:.4f} seconds:'.format(end_time - start_time))
                for row in solution:
                    print(','.join(row))
                return
        print('No solution found.')


class BacktrackingGemHunter:
    def __init__(self):
        self.board = []
        self.n = 0  # Number of rows
        self.m = 0  # Number of columns
        
    def gen_board(self, filepath: str) -> None:
        with open(filepath, 'r') as f:
            lines = f.readlines()
            for line in lines:
                row = line.strip().split(', ')
                self.board.append(row)
                self.n += 1  # Number of rows
                self.m = len(row)  # Number of columns
                
        # Print the board
        print('Input:')
        for row in self.board:
            print(','.join(row))
        print()
        
    def convert_to_cnf(self) -> List[List[Tuple[int, bool]]]:
        cnf_clauses = []
        for i in range(self.n):
            for j in range(self.m):
                if self.board[i][j] == '_':
                    # For each empty cell, generate clauses for each possibility (trap or gem)
                    clauses = []
                    # Add clause for trap
                    clauses.append((self.get_variable_index(i, j, is_trap=True), True))
                    # Add clause for gem
                    clauses.append((self.get_variable_index(i, j, is_trap=False), True))
                    cnf_clauses.append(clauses)
                elif self.board[i][j] != ' ':  # If the cell is not empty
                    # Enforce that the number of neighboring traps matches the number indicated in the cell
                    num_traps = int(self.board[i][j])
                    neighbor_indices = self.get_neighbor_indices(i, j)
                    clauses = []
                    for neighbor_index in neighbor_indices:
                        clauses.append((neighbor_index, True))
                    clauses.append((self.get_variable_index(i, j, is_trap=True), False))
                    cnf_clauses.append(clauses)
                    cnf_clauses.append([(self.get_variable_index(i, j, is_trap=True), True)] + \
                                        [(neighbor_index, False) for neighbor_index in neighbor_indices])
        return cnf_clauses
    
    def get_variable_index(self, i: int, j: int, is_trap: bool) -> int:
        # Each variable is represented by an integer
        return i * self.m + j + 1 if is_trap else (self.n * self.m) + i * self.m + j + 1
    
    def get_neighbor_indices(self, i: int, j: int) -> List[int]:
        neighbor_indices = []
        for di in [-1, 0, 1]:
            for dj in [-1, 0, 1]:
                if di == 0 and dj == 0:
                    continue
                if 0 <= i + di < self.n and 0 <= j + dj < self.m:
                    neighbor_indices.append(self.get_variable_index(i + di, j + dj, is_trap=True))
        return neighbor_indices
    
    def dpll(self, cnf: List[List[Tuple[int, bool]]], assignment: List[bool]) -> bool:
        depth = 0
        stack = [(cnf, assignment, depth)]
        
        while stack:
            cnf, assignment, depth = stack.pop()
            if depth > 1000:  # Add a depth limit to prevent infinite loop
                return False
            if not cnf:
                return True
            if any(len(clause) == 0 for clause in cnf):
                continue
            
            unit_clauses = [clause[0] for clause in cnf if len(clause) == 1]
            if unit_clauses:
                unit_clause = unit_clauses[0]
                variable, value = abs(unit_clause[0]), unit_clause[1]
                assignment[variable - 1] = value
                cnf = [clause for clause in cnf if unit_clause not in clause]
                stack.append((cnf, assignment, depth + 1))
            else:
                variable = abs(cnf[0][0][0])
                assignment[variable - 1] = True
                cnf_true = [clause for clause in cnf if variable not in clause]
                stack.append((cnf_true, assignment[:], depth + 1))
                
                assignment[variable - 1] = False
                cnf_false = [clause for clause in cnf if -variable not in clause]
                stack.append((cnf_false, assignment[:], depth + 1))
                
        return False
        
    def solve(self) -> List[List[str]]:
        cnf_clauses = self.convert_to_cnf()
        assignment = [False] * (self.n * self.m * 2)
        if self.dpll(cnf_clauses, assignment):
            solution = [['' for _ in range(self.m)] for _ in range(self.n)]
            for i in range(self.n):
                for j in range(self.m):
                    if self.board[i][j] == '_':
                        if assignment[self.get_variable_index(i, j, is_trap=True) - 1]:
                            solution[i][j] = 'T'
                        else:
                            solution[i][j] = 'G'
                    else:
                        solution[i][j] = self.board[i][j]
            return solution
        else:
            return None

# # Example usage
# if __name__ == '__main__':
#     gem_hunter = BacktrackingGemHunter()
#     gem_hunter.gen_board('test1.txt')
    
#     start_time = time.time()
#     result = gem_hunter.solve()
#     end_time = time.time()
    
#     if result:
#         print('Solution:')
#         for row in result:
#             print(','.join(row))
#     else:
#         print('No solution found.')
    
#     print("Execution time: {} seconds".format(end_time - start_time))


if __name__ == '__main__':
    brute_force_gem_hunter = BruteForceGemHunter()
    brute_force_gem_hunter.gen_board('test1.txt')
    brute_force_gem_hunter.brute_force_solve()
