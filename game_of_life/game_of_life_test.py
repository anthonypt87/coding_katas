import mock
import unittest

import game_of_life


class BoardCreationTest(unittest.TestCase):

    def test_create_empty_board_and_check_location(self):
        board = game_of_life.Board(1, 1)
        self.assertEqual(board[0, 0], False)

    def test_board_with_valid_cell(self):
        board = game_of_life.Board(1, 2, live_cells=[(0, 1)])
        self.assertEqual(board[0, 1], True)

    def test_cant_create_live_cells_out_of_bounds(self):
        for invalid_cell in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            with self.assertRaises(game_of_life.InvalidBoardError):
                game_of_life.Board(1, 1, live_cells=[invalid_cell])


class BoardStepTest(unittest.TestCase):

    def test_step_with_dead_cell_at_edge(self):
        board = self._create_board_and_step(1, 1)
        self.assertEqual(board[0, 0], False)

    def _create_board_and_step(self, *args, **kwargs):
        board = game_of_life.Board(*args, **kwargs)
        board.step()
        return board

    def test_step_with_live_cell_at_edge(self):
        board = self._create_board_and_step(1, 1, live_cells=[(0, 0)])
        self.assertEqual(board[0, 0], False)

    def test_three_live_cells_in_proximity_keep_you_alive(self):
        board = self._create_2_3_board_and_step(
            live_cells=[(0, 0), (0, 1), (0, 2)]
        )
        self.assertEqual(board[1, 1], True)

    def _create_2_3_board_and_step(self, live_cells):
        return self._create_board_and_step(2, 3, live_cells=live_cells)

    def test_four_cells_in_proximity_if_dead_leave_you_dead(self):
        board = self._create_2_3_board_and_step(
            live_cells=[(0, 0), (0, 1), (0, 2), (1, 0)]
        )
        self.assertEqual(board[1, 1], False)

    def test_four_cells_in_proximity_if_alive_keeps_you_alive(self):
        board = self._create_2_3_board_and_step(
            live_cells=[(0, 0), (0, 1), (0, 2), (1, 1)]
        )
        self.assertEqual(board[1, 1], True)

    def test_overpopulation_leads_to_death(self):
        board = self._create_2_3_board_and_step(
            live_cells=[(0, 0), (0, 1), (0, 2), (1, 2), (1, 1)]
        )
        self.assertEqual(board[1, 1], False)


class BoardEqualTest(unittest.TestCase):

    def test_equal(self):
        board_1 = game_of_life.Board(1, 1)
        board_2 = game_of_life.Board(1, 1, live_cells=[(0, 0)])
        board_3 = game_of_life.Board(1, 1)
        self.assertNotEqual(board_1, board_2)
        self.assertEqual(board_1, board_3)


class BoardLoaderFromInputTest(unittest.TestCase):

    def test_load_from_input(self):
        board = self._create_board_with_mock_input_function("0 0 0 0\n0 1 0 0")
        self.assertEqual(
            board,
            game_of_life.Board(4, 2, live_cells=[(1, 1)])
        )

    def _create_board_with_mock_input_function(self, input_return_value):
        board_loader = game_of_life.BoardLoaderFromInput(
            input_function=mock.Mock(
                return_value=input_return_value
            )
        )
        return board_loader.load()

    def test_non_0_1_values_raises_invalid_board(self):
        self._check_invalid_input_raises_exception("0 0 0 0\n0 1 k 0")

    def _check_invalid_input_raises_exception(self, input_return_value):
        with self.assertRaises(game_of_life.InvalidBoardError):
            self._create_board_with_mock_input_function(input_return_value)

    def test_inconsistent_length_raises_invalid_board(self):
        self._check_invalid_input_raises_exception("0 0\n0 1 k 0")

    def test_non_positive_length_raises_invalid_board(self):
        self._check_invalid_input_raises_exception("")

    def test_non_positive_x_length_raises_exception(self):
        self._check_invalid_input_raises_exception("\n1")


class BoardDrawerTest(unittest.TestCase):

    def test_draw_board(self):
        board = game_of_life.Board(2, 2, live_cells=[(0, 1)])
        mock_print = mock.Mock()
        game_of_life.BoardDrawer(print_function=mock_print).draw(board)
        self.assertEqual(
            mock_print.call_args_list,
            [
                (('',),),
                (('0 0',),),
                (('1 0',),),
            ]
        )


if __name__ == '__main__':
    unittest.main()
