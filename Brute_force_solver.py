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
                    for di, dj in itertools.product([-1, 0, 1], repeat=2): # 8 directions
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