from sudoku import Sudoku
from solver import SudokuSolver
import itertools

easy_sudoku = Sudoku()

easy_sudoku[1, 1] = 2
easy_sudoku[1, 2] = 6
easy_sudoku[2, 2] = 8
easy_sudoku[2, 3] = 9
easy_sudoku[3, 2] = 7
easy_sudoku[3, 3] = 1
easy_sudoku[2, 5] = 6
easy_sudoku[3, 6] = 8
easy_sudoku[3, 7] = 6
easy_sudoku[3, 8] = 9
easy_sudoku[3, 9] = 4
easy_sudoku[4, 3] = 6
easy_sudoku[4, 5] = 9
easy_sudoku[4, 6] = 4
easy_sudoku[4, 7] = 8
easy_sudoku[4, 9] = 5
easy_sudoku[5, 3] = 4
easy_sudoku[5, 4] = 8
easy_sudoku[5, 6] = 7
easy_sudoku[5, 7] = 9
easy_sudoku[6, 1] = 1
easy_sudoku[6, 3] = 8
easy_sudoku[6, 4] = 6
easy_sudoku[6, 5] = 3
easy_sudoku[6, 7] = 4
easy_sudoku[7, 1] = 9
easy_sudoku[7, 2] = 5
easy_sudoku[7, 3] = 3
easy_sudoku[7, 7] = 1
easy_sudoku[7, 8] = 4
easy_sudoku[8, 5] = 1
easy_sudoku[8, 7] = 5
easy_sudoku[8, 8] = 7
easy_sudoku[9, 8] = 8
easy_sudoku[9, 9] = 9

slvr = SudokuSolver(easy_sudoku)

medium_sudoku = Sudoku.from_list([
    None, None, None,    6, None, None,    4, None, None,
    None,    5,    2, None,    3, None, None,    8, None,
       4, None, None,    5, None, None,    7, None, None,
       5, None,    1, None, None, None, None,    4, None,
       7, None, None,    3, None,    6, None, None,    8,
    None,    2, None, None, None, None,    1, None,    7,
    None, None,    6, None, None,    5, None, None,    1,
    None,    4, None, None,    6, None,    9,    7, None,
    None, None,    5, None, None,    7, None, None, None])

if __name__ == '__main__':

    print("Easy Sudoku")
    print(easy_sudoku)
    slvr.solve()
    print(easy_sudoku)

    print("Medium sudoku:")
    print(medium_sudoku)
    slvr = SudokuSolver(medium_sudoku)
    slvr.solve()
    print(medium_sudoku)
