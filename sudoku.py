"""A sudoku solver in python."""

import numbers


class SudokuIntegrityError(Exception):
    pass


class SquareBoard(object):
    """Class representing a two-dimensional square board.

    >>> tictactoe = SquareBoard(3)
    >>> tictactoe
    SquareBoard(dimension=3)
    >>> tictactoe[1, 1] is None
    True
    >>> tictactoe[2, 2] = 'X'
    >>> tictactoe[2, 2]
    'X'
    >>> tictactoe[1]
    Traceback (most recent call last):
    ...
    TypeError: board positions must be a sequence of 2 integers
    >>> tictactoe[1, 3, 1] = 4
    Traceback (most recent call last):
    ...
    TypeError: board positions must be a sequence of 2 integers
    >>> tictactoe[1, 3] = 'O'
    >>> tictactoe.row(1)
    [None, None, 'O']
    >>> tictactoe.col(1)
    [None, None, None]
    >>> print(tictactoe)
    +---+---+---+
    |   |   | O |
    +---+---+---+
    |   | X |   |
    +---+---+---+
    |   |   |   |
    +---+---+---+

    >>> sudoku = SquareBoard(9)
    >>> print(sudoku)
    +---+---+---+---+---+---+---+---+---+
    |   |   |   |   |   |   |   |   |   |
    +---+---+---+---+---+---+---+---+---+
    |   |   |   |   |   |   |   |   |   |
    +---+---+---+---+---+---+---+---+---+
    |   |   |   |   |   |   |   |   |   |
    +---+---+---+---+---+---+---+---+---+
    |   |   |   |   |   |   |   |   |   |
    +---+---+---+---+---+---+---+---+---+
    |   |   |   |   |   |   |   |   |   |
    +---+---+---+---+---+---+---+---+---+
    |   |   |   |   |   |   |   |   |   |
    +---+---+---+---+---+---+---+---+---+
    |   |   |   |   |   |   |   |   |   |
    +---+---+---+---+---+---+---+---+---+
    |   |   |   |   |   |   |   |   |   |
    +---+---+---+---+---+---+---+---+---+
    |   |   |   |   |   |   |   |   |   |
    +---+---+---+---+---+---+---+---+---+
    """

    def __init__(self, dimension):
        self.dimension = int(dimension)
        self._board = [None for x in range(self.dimension ** 2)]

    def __repr__(self):
        clsname = type(self).__name__
        return "{}(dimension={})".format(clsname, self.dimension)

    def __str__(self):
        """Print the board."""
        bars = '+---' * self.dimension + '+'
        spaces = "| {} " * self.dimension + '|'
        retval = []
        for i in range(1, self.dimension + 1):
            retval.append(bars)
            retval.append(spaces.format(*[x or ' ' for x in self.row(i)]))
        retval.append(bars)
        return '\n'.join(retval)

    def _colmajor(self, row, col):
        """For a row and column, return the corresponding index
        of a one-dimensional array in column major order."""
        if (row > self.dimension or row < 1 or
           col > self.dimension or col < 1):
                errmsg = '({}, {}) out of bounds'.format(row, col)
                raise ValueError(errmsg)
        return (row - 1) + (col - 1) * self.dimension

    def _rowmajor(self, row, col):
        """For a row and column, return the corresponding index
        of a one-dimensional array in row major order."""
        if (row > self.dimension or row < 1 or
           col > self.dimension or col < 1):
                errmsg = '({}, {}) out of bounds'.format(row, col)
                raise ValueError(errmsg)
        return (col - 1) + (row - 1) * self.dimension

    def row(self, row):
        """Return a row of the board in a list."""
        return [self._board[self._rowmajor(row, i + 1)]
                for i in range(self.dimension)]

    def col(self, col):
        """Return a column of the board in a list."""
        return [self._board[self._rowmajor(i + 1, col)]
                for i in range(self.dimension)]

    def __getitem__(self, position):
        try:
            return self._board[self._rowmajor(*position)]
        except TypeError as exc:
            errmsg = 'board positions must be a sequence of 2 integers'
            raise TypeError(errmsg)

    def __setitem__(self, position, value):
        try:
            self._board[self._rowmajor(*position)] = value
        except TypeError as exc:
            errmsg = 'board positions must be a sequence of 2 integers'
            raise TypeError(errmsg) from exc


class Sudoku(SquareBoard):
    """A class representing a sudoku puzzle

    >>> sudoku = Sudoku(9)
    >>> sudoku[3,5] = 10
    Traceback (most recent call last):
    ...
    ValueError: 10 is not a legal value for this sudoku
    >>> sudoku[3,5] = 8
    >>> print(sudoku)
    +---+---+---+---+---+---+---+---+---+
    |   |   |   |   |   |   |   |   |   |
    +---+---+---+---+---+---+---+---+---+
    |   |   |   |   |   |   |   |   |   |
    +---+---+---+---+---+---+---+---+---+
    |   |   |   |   | 8 |   |   |   |   |
    +---+---+---+---+---+---+---+---+---+
    |   |   |   |   |   |   |   |   |   |
    +---+---+---+---+---+---+---+---+---+
    |   |   |   |   |   |   |   |   |   |
    +---+---+---+---+---+---+---+---+---+
    |   |   |   |   |   |   |   |   |   |
    +---+---+---+---+---+---+---+---+---+
    |   |   |   |   |   |   |   |   |   |
    +---+---+---+---+---+---+---+---+---+
    |   |   |   |   |   |   |   |   |   |
    +---+---+---+---+---+---+---+---+---+
    |   |   |   |   |   |   |   |   |   |
    +---+---+---+---+---+---+---+---+---+
"""

    def __setitem__(self, position, value):
        value = int(value)
        if value < 1 or value > self.dimension:
            errmsg = '{} is not a legal value for this sudoku'.format(value)
            raise ValueError(errmsg)
        else:
            super(Sudoku, self).__setitem__(position, value)
