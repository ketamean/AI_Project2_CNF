import copy
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
        self.id_board = [[0] * m for i in range(n)]
        self.marked_board = copy.deepcopy(self.id_board)
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
                        self.marked_board[x][y] = 1
                    elif self.main_board[x][y] == 'T':
                        num_trap_cells -= 1
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
                    self.result_clauses.append([self.id_board[i][j]] * -1)
        return self.result_clauses
