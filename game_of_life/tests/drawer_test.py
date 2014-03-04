import unittest

from game_of_life import drawer
from game_of_life.board import Board


class DrawerTest(unittest.TestCase):

    def test_draw_board(self):
        board = Board(2, 2, live_cells=[(0, 1)])
        results = drawer.Drawer().draw(board)
        self.assertEqual(results, '0 0\n1 0')


if __name__ == '__main__':
    unittest.main()
