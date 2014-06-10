"""Solving the old 8 queens problem"""
import unittest
import mock


def place_queens(board_size, number_of_queens, valid_move_checker=None):
    board = Board(board_size)
    valid_move_checker = valid_move_checker or ValidMoveChecker()
    while True:
        board, number_of_queens, next_queen_postion




class ValidMoveChecker(object):
    def is_valid_move(self, board):
        pass


class Board(object):

    def __init__(self, size):
        self._board = [[False] * size] * size

    def has_queen(self, x, y):
        return self._board[x][y]

    def set_queen(self, x, y):
        self._board[x][y] = True


class BoardTest(unittest.TestCase):

    def test_board_isntantiation(self):
        Board(3)

    def test_set_and_get_queen(self):
        board = Board(3)
        self.assertEqual(board.has_queen(1, 2), False)
        board.set_queen(1, 2)
        self.assertEqual(board.has_queen(1, 2), True)


class PlaceQueensIntegrationTest(unittest.TestCase):

    def test_place_queens_correctly(self):
        expected_number_of_queens = board_size = 3
        result_board = place_queens(board_size, expected_number_of_queens)

        number_of_queens = sum(
            1 for x in xrange(board_size) for y in xrange(board_size)
            if result_board.has_queen(x, y)
        )
        self.assertEqual(number_of_queens, expected_number_of_queens)


class PlaceQueensUnitTest(unittest.TestCase):

    def test_place_only_if_valid(self):
        mock_valid_move_checker = mock.Mock()
        mock_valid_move_checker.check_move.side_effect = [True, False, True]
        result_board = place_queens(3, 2, mock_valid_move_checker)
        self.assertEqual(result_board.has_queen(0, 0), True)
        self.assertEqual(result_board.has_queen(0, 2), True)


if __name__ == '__main__':
    unittest.main()
