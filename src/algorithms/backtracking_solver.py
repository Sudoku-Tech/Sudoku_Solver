class BacktrackingSolver:
    def __init__(self, board):
        self.board = [row[:] for row in board]  # Copia del tablero original
        self.steps = []      # [(fila, col, valor)]
        self.backtracks = 0

    def solve(self):
        self._solve_internal()

    def _solve_internal(self):
        empty = self._find_empty()
        if not empty:
            return True 

        row, col = empty
        for num in range(1, 10):
            if self._is_valid(row, col, num):
                self.board[row][col] = num
                self.steps.append((row, col, num))

                if self._solve_internal():
                    return True

                self.board[row][col] = 0
                self.backtracks += 1
                self.steps.append((row, col, 0))  

        return False

    def _find_empty(self):
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    return i, j
        return None

    def _is_valid(self, row, col, num):
        # Verifica fila y columna
        for i in range(9):
            if self.board[row][i] == num or self.board[i][col] == num:
                return False

        # Verifica subcuadro 3x3
        box_x = (col // 3) * 3
        box_y = (row // 3) * 3
        for i in range(box_y, box_y + 3):
            for j in range(box_x, box_x + 3):
                if self.board[i][j] == num:
                    return False

        return True
