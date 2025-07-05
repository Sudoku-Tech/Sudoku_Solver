import itertools

class BruteForceSolver:
    def __init__(self, board):
        self.board = [row[:] for row in board]
        self.steps = []      # [(fila, col, valor)]
        self.backtracks = 0

    def solve(self):
        self._brute_force()

    def _brute_force(self):
        empty_cells = [(i, j) for i in range(9) for j in range(9) if self.board[i][j] == 0]
        return self._try_combinations(empty_cells, 0)

    def _try_combinations(self, cells, idx):
        if idx == len(cells):
            return True  # Resuelto

        i, j = cells[idx]
        for num in range(1, 10):
            if self._is_valid(i, j, num):
                self.board[i][j] = num
                self.steps.append((i, j, num))

                if self._try_combinations(cells, idx + 1):
                    return True

                self.board[i][j] = 0
                self.backtracks += 1
                self.steps.append((i, j, 0))  
        return False

    def _is_valid(self, row, col, num):
        for i in range(9):
            if self.board[row][i] == num or self.board[i][col] == num:
                return False

        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if self.board[i][j] == num:
                    return False
        return True
