from sudoku import Sudoku, SudokuIntegrityError


class SudokuSolver(object):
    strategies = []

    def __init__(self, sudoku):
        if not isinstance(sudoku, Sudoku):
            clsname = type(self).__name__
            errmsg = 'Constructor for {} takes type Sudoku'.format(clsname)
            raise TypeError()
        self.puzzle = sudoku
        self.possibilities = []
        for i in range(1, self.puzzle.dimension + 1):
            self.possibilities.append({pos for value, pos in self.puzzle})
        self.updates = set()

    def solve(self):
        """Solve a sudoku puzzle."""
        dim = self.puzzle.dimension

        # initial loop
        for value, (row, col) in self.puzzle:
            if value:
                self.clear_row(row, value)
                self.clear_col(col, value)
                self.clear_subgrid(row, col, value)
                self.updates.add((value, (row, col)))

        while self.updates:
            while self.updates:
                # while self.updates:
                val, (row, col) = self.updates.pop()
                for i in range(1, dim + 1):
                    self.check_row(i, value)
                    self.check_col(i, value)
                for i in range(2, 8, 3):
                    self.check_subgrid(row, i, value)
                    self.check_subgrid(i, col, value)

            for value, (row, col) in self.puzzle:
                if not value:
                    self.check_cell(row, col)

    def update_cell(self, row, col, value):
        self.clear_row(row, value)
        self.clear_col(col, value)
        self.clear_subgrid(row, col, value)
        self.puzzle[row, col] = value
        self.updates.add((value, (row, col)))
        for ps in self.possibilities:
            ps.discard((row, col))

    def check_cell(self, row, col):
        possible_values = [
            value for value, pos in enumerate(self.possibilities, start=1)
            if (row, col) in pos]
        if len(possible_values) == 0:
            if not self.puzzle[row, col]:
                raise(SudokuIntegrityError)
        elif len(possible_values) == 1:
            value = possible_values.pop()
            self.update_cell(row, col, value)

    def clear_row(self, row, value):
        for pos in self.puzzle.row_positions(row):
            self.possibilities[value - 1].discard(pos)

    def clear_col(self, col, value):
        for pos in self.puzzle.col_positions(col):
            self.possibilities[value - 1].discard(pos)

    def clear_subgrid(self, row, col, value):
        for pos in self.puzzle.subgrid_positions(row, col):
            self.possibilities[value - 1].discard(pos)

    def check_row(self, row, value):
        _row = self.puzzle.row_positions(row)
        intersect = _row & self.possibilities[value - 1]
        if len(intersect) == 1:
            row, col = next(iter(intersect))
            self.update_cell(row, col, value)

    def check_col(self, col, value):
        _col = self.puzzle.col_positions(col)
        intersect = _col & self.possibilities[value - 1]
        if len(intersect) == 1:
            row, col = next(iter(intersect))
            self.update_cell(row, col, value)

    def check_subgrid(self, row, col, value):
        _sub = self.puzzle.subgrid_positions(row, col)
        intersect = _sub & self.possibilities[value - 1]
        if len(intersect) == 1:
            row, col = next(iter(intersect))
            self.update_cell(row, col, value)
