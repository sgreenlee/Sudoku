"""A sudoku solver in python."""

import numbers
import functools
import math


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
    TypeError: __getitem__ indexes must be a sequence of 2 integers or slices
    >>> tictactoe[1, 3, 1] = 4
    Traceback (most recent call last):
    ...
    TypeError: __setitem__ indexes must be a sequence of 2 integers
    >>> tictactoe[1, 3] = 'O'
    >>> for value, (row, col) in tictactoe:
    ...    if value:
    ...        print("tictactoe[{}, {}] = {}".format(row, col, value))
    tictactoe[1, 3] = O
    tictactoe[2, 2] = X
    >>> tictactoe.row(1)
    [None, None, 'O']
    >>> tictactoe.row_values(1)
    frozenset({'O'})
    >>> tictactoe.col(1)
    [None, None, None]
    >>> tictactoe.col_values(1)
    frozenset()
    >>> print(tictactoe)
    +---+---+---+
    |   |   | O |
    +---+---+---+
    |   | X |   |
    +---+---+---+
    |   |   |   |
    +---+---+---+
    >>> tictactoe2 = SquareBoard.from_list(['X', 'X', 'O', 'O', 'O', 'X', 'X', 'X', 'O'])
    >>> print(tictactoe2)
    +---+---+---+
    | X | X | O |
    +---+---+---+
    | O | O | X |
    +---+---+---+
    | X | X | O |
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
        self.__rows = []
        for i in range(1, self.dimension + 1):
            self.__rows.append(
                frozenset((i, j) for j in range(1, self.dimension + 1)))
        self.__cols = []
        for j in range(1, self.dimension + 1):
            self.__cols.append(
                frozenset((i, j) for i in range(1, self.dimension + 1)))

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

    @classmethod
    def from_list(cls, lst):
        """Instantiate a board from a list of values."""
        dim = int(math.sqrt(len(lst)))
        if dim * dim != len(lst):
            raise ValueError('length of list must be a square number')
        new = cls(dim)
        new._board = lst
        return new

    def __len__(self):
        return self.dimension ** 2

    def __iter__(self):
        return ((self[row, col], (row, col))
                for row in range(1, self.dimension + 1)
                for col in range(1, self.dimension + 1))

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

    def row_values(self, row):
        """Return a frozenset of the values in row i of the board."""
        return frozenset(self[row, j] for j in range(1, self.dimension + 1)
                         if self[row, j])

    def col_values(self, col):
        """Returns a frozenset of the values in col i of the board."""
        return frozenset(self[i, col] for i in range(1, self.dimension + 1)
                         if self[i, col])

    def row(self, row):
        """Return a list of values in the given row of the board."""
        return self[row, 1:(self.dimension + 1)]

    def col(self, col):
        """Return a list of values in the given row of the board."""
        return self[1:(self.dimension + 1), col]

    def row_positions(self, i):
        """Return a frozenset of positions in row i of the board."""
        return self.__rows[i - 1]

    def col_positions(self, col):
        """Return a frozenset of positions in col i of the board."""
        return self.__cols[col - 1]

    def __getitem__(self, position):
        try:
            x, y = position
            if isinstance(x, slice) or isinstance(y, slice):
                if isinstance(x, slice):
                    if x.step:
                        rows = range(x.start, x.stop, x.step or None)
                    else:
                        rows = range(x.start, x.stop)
                else:
                    rows = (x,)
                if isinstance(y, slice):
                    if y.step:
                        cols = range(y.start, y.stop, y.step or None)
                    else:
                        cols = range(y.start, y.stop)
                else:
                    cols = (y,)
                return [self._board[self._rowmajor(row, col)] for row in rows
                        for col in cols]
            else:
                return self._board[self._rowmajor(x, y)]
        except TypeError as exc:
            errmsg = ('__getitem__ indexes must be a sequence of 2 integers'
                      ' or slices')
            raise TypeError(errmsg) from exc

    def __setitem__(self, position, value):
        try:
            self._board[self._rowmajor(*position)] = value
        except TypeError as exc:
            errmsg = '__setitem__ indexes must be a sequence of 2 integers'
            raise TypeError(errmsg) from exc


class Sudoku(SquareBoard):
    """A class representing a sudoku puzzle

    >>> sudoku = Sudoku()
    >>> sudoku
    Sudoku(dimension=9)
    >>> sudoku[3, 5] = 10
    Traceback (most recent call last):
    ...
    ValueError: 10 is not a legal value for this sudoku
    >>> sudoku[3, 5] = 8
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
    >>> sudoku.subgrid(3, 5)
    [None, None, None, None, None, None, None, 8, None]
    >>> sudoku[9, 1] = 4
    >>> sudoku.subgrid(7, 3)
    [None, None, None, None, None, None, 4, None, None]
    >>> sudoku[1, 4] = 8
    Traceback (most recent call last):
    ...
    sudoku.SudokuIntegrityError: illegal value for this cell

"""

    def __init__(self):
        dimension = 9
        super(Sudoku, self).__init__(dimension)
        self.__subgrids = []
        for i in range(self.dimension // 3):
            for j in range(self.dimension // 3):
                x = j * 3 + 1
                y = i * 3 + 1
                self.__subgrids.append(
                    frozenset((row, col) for row in range(y, y + 3)
                              for col in range(x, x + 3)))

    def subgrid(self, row, col):
        """Return the items in the subgrid containing cell (row, col)"""
        x = ((col - 1) // 3) * 3 + 1
        y = ((row - 1) // 3) * 3 + 1
        rows = slice(y, y + 3)
        cols = slice(x, x + 3)
        return self[rows, cols]

    def subgrid_positions(self, row, col):
        index = ((col - 1) // 3) + 3 * ((row - 1) // 3)
        return self.__subgrids[index]

    def subgrid_values(self, row, col):
        """Return frozenset of values in subgrid of board containing given
        row and column."""
        return frozenset(self[pos] for pos in self.subgrid_positions(row, col)
                         if self[pos])

    def __setitem__(self, position, value):
        value = int(value)
        row, col = position
        if value < 1 or value > self.dimension:
            errmsg = '{} is not a legal value for this sudoku'.format(value)
            raise ValueError(errmsg)
        # check for puzzle integrity errors
        elif (value in self.row_values(row) or
              value in self.col_values(col) or
              value in self.subgrid_values(row, col)):
                raise SudokuIntegrityError('illegal value for this cell')
        else:
            super(Sudoku, self).__setitem__(position, value)



        # initialize updates
