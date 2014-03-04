# -*- coding: utf-8 -*-
class Drawer(object):
    """Responsible for drawing the board"""

    def draw(self, board):
        """Draws and prints a `board`

        Args:
            board - `Board` object to print

        Example:
        Given the board, Board(2, 2, live_cells=[(1, 1)]), prints the
        following:
            '0 0\n0 1'
        """
        rows = []
        for y in xrange(board.y_size):
            row = ' '.join(
                '1' if board[x, y] else '0' for x in xrange(board.x_size)
            )
            rows.append(row)

        return '\n'.join(rows)
