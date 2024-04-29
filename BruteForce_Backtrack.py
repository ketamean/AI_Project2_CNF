import itertools
import time

# Brute Force Gem Hunter
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
                return (end_time - start_time), solution
        return None, None
    
    def print_solution(self, run_time, solution):
        if solution:
            print('Solution found in {:.4f} seconds:'.format(run_time))
            for row in solution:
                print(','.join(row))
        else:
            print('No solution found.')

# Backtracking
class BacktrackingGemHunter:
    def __init__(self):
        self.board = []
        self.n = 0  # Number of rows
        self.m = 0  # Number of columns

    def gen_board(self, filepath):
        with open(filepath, 'r') as f:
            lines = f.readlines()
            for line in lines:
                row = [None if x.strip() == '_' else int(x.strip()) for x in line.strip().split(',')]
                self.board.append(row)
                self.n += 1  # Number of rows
                self.m = len(row)  # Number of columns

        # # Print the board
        # print('Input:')
        # for row in self.board:
        #     print(','.join([str(cell) if cell is not None else '_' for cell in row]))
        # print()

    def get_neighbors(self, i, j):
        return [(x, y) for x in range(max(0, i-1), min(self.n, i+2))
                for y in range(max(0, j-1), min(self.m, j+2)) if (x != i or y != j)]

    def is_valid(self, i, j, value, assignments):
        temp_assignments = assignments.copy()
        temp_assignments[(i, j)] = value
        for ni, nj in self.get_neighbors(i, j):
            if isinstance(self.board[ni][nj], int):
                expected_traps = self.board[ni][nj]
                neighbors = self.get_neighbors(ni, nj)
                count = sum(temp_assignments.get((nii, nij), False) for nii, nij in neighbors)
                if count > expected_traps or (all((nii, nij) in temp_assignments for nii, nij in neighbors) and count != expected_traps):
                    return False
        return True

    def backtrack(self, assignments):
        if len(assignments) == sum(1 for row in self.board for cell in row if cell is None):
            return True

        unassigned = [(i, j) for i in range(self.n) for j in range(self.m) if self.board[i][j] is None and (i, j) not in assignments]
        if not unassigned:
            return True
        i, j = min(unassigned, key=lambda x: -len([1 for ni, nj in self.get_neighbors(x[0], x[1]) if isinstance(self.board[ni][nj], int)]))

        for value in [True, False]:  # True for Trap, False for Gem
            if self.is_valid(i, j, value, assignments):
                assignments[(i, j)] = value
                if self.backtrack(assignments):
                    return True
                del assignments[(i, j)]
        return False

    def solve(self):
        start_time = time.time()
        assignments = {}
        if self.backtrack(assignments):
            end_time = time.time()
            return (end_time - start_time), assignments
        return None, None

    def print_solution(self, run_time, solution):
        if solution:
            print('Solution found in {:.4f} seconds:'.format(run_time))
            final_output = [['_' for _ in range(self.m)] for _ in range(self.n)]

            # Fill the solution into the final output
            for i, row in enumerate(self.board):
                for j, cell in enumerate(row):
                    if cell is None:
                        final_output[i][j] = 'T' if solution.get((i, j), False) else 'G'
                    else:
                        final_output[i][j] = str(cell)

            # Check for cells with no number neighbors and adjust if necessary
            for row in range(self.n):
                for col in range(self.m):
                    if self.board[row][col] is None:
                        has_number_neighbor = any(isinstance(self.board[ni][nj], int) for ni, nj in self.get_neighbors(row, col))
                        if not has_number_neighbor:
                            final_output[row][col] = 'G'  # Ensure cells with no number neighbors are Gems

            # Print the final adjusted board
            for row in final_output:
                print(','.join(row))
        else:
            print("No solution found.")


if __name__ == '__main__':
    backtracking_gem_hunter = BacktrackingGemHunter()
    brute_force_gem_hunter = BruteForceGemHunter()

    backtracking_gem_hunter.gen_board('test3.txt')
    brute_force_gem_hunter.gen_board('test3.txt')

    print('Backtracking:')
    run_time, solution = backtracking_gem_hunter.solve()
    backtracking_gem_hunter.print_solution(run_time, solution)

    print('\nBrute Force:')
    run_time, solution = brute_force_gem_hunter.brute_force_solve()
    brute_force_gem_hunter.print_solution(run_time, solution)

