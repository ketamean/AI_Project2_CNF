import copy

#-----------------BoardCNF.py-----------------
"""
This class provides a way to encode the Gem Hunter puzzle as a CNF formula and generate the clauses needed to solve the puzzle using a SAT solver.
How this class works:
1. The main_board attribute is a 2D list that contains the current board.
2. The n and m attributes store the number of rows and columns in the board.
3. The id_board attribute is a 2D list that stores the unique identifier for each cell in the board.
4. The marked_board attribute is a 2D list that keeps track of which cells have been marked as traps.
5. The result_clauses attribute is a list that stores the CNF clauses generated from the board.
6. The update_board method updates the current board with a new board.
7. The gen_combine method generates all possible combinations of trap cells given the number of traps and their positions.
8. The add_cells_clauses method adds clauses for each cell that contains a number.
9. The gen_clauses method generates the CNF clauses from the current board.
"""

class BoardCNF:
    def __init__(self, board: list, n: int, m: int):
        self.main_board = []
        for row in board:
            m_row = []
            for item in row:
                if '0' <= item <= '9':
                    m_row.append(int(item)) # Convert string to int
                else:
                    m_row.append(item)
            self.main_board.append(m_row)
        self.n = n # Number of rows
        self.m = m # Number of columns
        self.id_board = [[0] * m for i in range(n)]
        self.marked_board = copy.deepcopy(self.id_board)
        self.result_clauses = []
        for i in range(0, n):
            for j in range(0, m):
                self.id_board[i][j] = i * m + j + 1 # Assign a unique identifier to each cell (from 1 to n*m)

    def update_board(self, board: list):
        """ Update current main board to a new board."""
        self.main_board = copy.deepcopy(board)
        self.result_clauses = self.gen_clauses()

    @staticmethod
    def gen_combine(num_trap_cells: int, pos_trap_cells: list) -> list:
        """Generate all possible combinations of num_trap_cells in pos_trap_cells."""
        import itertools
        greater_equal = list(itertools.combinations(pos_trap_cells, len(pos_trap_cells) - num_trap_cells + 1)) # pos_trap_cells - num_trap_cells <= 1
        lower_equal = list(itertools.combinations(pos_trap_cells, num_trap_cells + 1))  # pos_trap_cells - num_trap_cells >= 1 
        combinations_clause = []
        for item in greater_equal: 
            combinations_clause.append(list(item)) # Convert tuple to list
        for item in lower_equal:
            neg_item = []
            for i in list(item):
                neg_item.append(-1 * i) # Negate the item
            combinations_clause.append(neg_item) # Append the negated item
        return combinations_clause 

    def add_cells_clauses(self, row: int, col: int) -> None:
        """Add clauses for each cell that contains a number."""
        pos_trap_cells = []
        num_trap_cells = self.main_board[row][col] # Number of traps around the cell
        for delta_row in range(-1, 2):
            for delta_col in range(-1, 2): # 8 directions
                x = row + delta_row # Neighbor row
                y = col + delta_col # Neighbor column
                if 0 <= x < self.n and 0 <= y < self.m:
                    if self.main_board[x][y] == '_':
                        pos_trap_cells.append(self.id_board[x][y]) # Add the neighbor cell to pos_trap_cells
                        self.marked_board[x][y] = 1 # Mark the neighbor cell
                    elif self.main_board[x][y] == 'T': # If the neighbor cell is a trap
                        num_trap_cells -= 1 # Decrement the number of traps
        clauses = self.gen_combine(num_trap_cells, pos_trap_cells)
        self.result_clauses.append([self.id_board[row][col] * -1]) 
        for clause in clauses:
            self.result_clauses.append(clause)

    def gen_clauses(self) -> list:
        """Gen clauses using current main board and return a list that contains all the clauses."""
        for i in range(0, self.n):
            for j in range(0, self.m):
                if type(self.main_board[i][j]) is int: 
                    self.add_cells_clauses(i, j)
        for i in range(0, self.n):
            for j in range(0, self.m):
                if self.main_board[i][j] == '_' and self.marked_board[i][j] == 0:
                    self.result_clauses.append([self.id_board[i][j] * -1]) # self.id_board[i][j] * -1 is the negation of the cell
        return self.result_clauses
