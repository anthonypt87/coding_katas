import time


class InvalidBoardError(Exception):
    pass


class GameRunner(object):

    _sleep_time = .25

    def __init__(self, board_loader=None, board_drawer=None):
        self._board_loader = board_loader or BoardLoaderFromInput()
        self._board_drawer = board_drawer or BoardDrawer()

    def run(self):
        board = self._board_loader.load()
        while True:
            self._board_drawer.draw(board)
            board.step()
            time.sleep(self._sleep_time)


def parse_input():
    """Parses user input separated by new lines until an empty string is passed
    in."""
    return '\n'.join(iter(raw_input, ''))


class BoardLoaderFromInput(object):
    """Loads and creates the Game of LIfe `Board` using the users input. A
    board should described as a string of 0's and 1's, 0's representing a dead
    cell, 1's representing a live cell. The cells should be delimited by spaces
    to represent seperate columns and newlines to represent seperate lows.

    Sample Valid Input:
    1 1 1 1 0
    0 1 1 0 0
    0 1 1 1 0
    """

    def __init__(self, input_function=parse_input):
        """Creates the `BoardLoaderFromInput`

        Keyword Args:
            input_function - injected dependency to that takes in a users
                `input_function` and returns a string
        """
        self._input_function = input_function

    def load(self):
        """Gets the raw string board using `input_function` and creates a
        `Board`."""
        lines = self._get_lines_from_input()

        if not lines:
            raise InvalidBoardError

        x_length, y_length = self._get_board_dimension_from_lines(lines)

        live_cells = []
        for y, line in enumerate(lines):
            values = self._get_values(line)

            if len(values) != x_length:
                raise InvalidBoardError

            for x, value in enumerate(values):
                if self._is_live_cell(value):
                    live_cells.append((x, y))

        return Board(x_length, y_length, live_cells=live_cells)

    def _get_lines_from_input(self):
        string_board = self._input_function()
        return string_board.splitlines()

    def _get_board_dimension_from_lines(self, lines):
        x_length = len(self._get_values(lines[0]))
        y_length = len(lines)
        return x_length, y_length

    def _get_values(self, line):
        return line.split(' ')

    def _is_live_cell(self, value):
        if value == '1':
            return True
        elif value == '0':
            return False
        else:
            raise InvalidBoardError


class Board(object):
    """Represents a Game of Life board.
    A board is described by it's dimensions, `x_size`, and `y_size`, and the
    live cells (`live_cells`) it contains. It knows how to progress itself to
    its next iteration through the `step()` function.
    """

    def __init__(self, x_size, y_size, live_cells=()):
        """Creates a new `Board` object.

        Args:
            x_size - integer describing the size of the x dimension
            y_size - integer describing the size of the y dimension

        Keyword Args:
            live_cells - iterable of (x, y) integer pairs representing live
                cells on the `Board` object.
        """
        self.x_size = x_size
        self.y_size = y_size
        self._live_cells = set(live_cells)
        self._ensure_live_cells_is_in_bounds()

    def _ensure_live_cells_is_in_bounds(self):
        for cell in self._live_cells:
            if not self._is_cell_in_bounds(cell):
                raise InvalidBoardError

    def _is_cell_in_bounds(self, (x, y)):
        x_is_in_bounds = 0 <= x < self.x_size
        y_is_in_bounds = 0 <= y < self.y_size
        return x_is_in_bounds and y_is_in_bounds

    def __getitem__(self, cell):
        """Gets the current status of a particular cell, returning `True` if
        the cell is alive and `False` if it is not.

        Args:
            cell - (x, y) integer tuple representing the position to check

        Note: The way Python works with `__getitem__()` allows you to do
        board[1, 2], returning you the value at position (1, 2).
        """
        return cell in self._live_cells

    def __eq__(self, board):
        """Returns `True` if the boards are the same, where equality is defined
        by having the same dimensions and live cells.

        Args:
            board - the `Board` object to compare `self` to
        """
        return self.x_size == board.x_size and \
            self.y_size == board.y_size and \
            self._live_cells == board._live_cells

    def step(self):
        """Steps the game board according to the following rules (borrowed from
        Wikipedia):

        1. Any live cell with fewer than two live neighbours dies, as if caused
            by under-population.
        2. Any live cell with two or three live neighbours lives on to the next
            generation.
        3. Any live cell with more than three live neighbours dies, as if by
            overcrowding.
        4. Any dead cell with exactly three live neighbours becomes a live
            cell, as if by reproduction.

        Updates `self._live_cells` to represent the new set of live cells after
        the current iteration.
        """
        self._live_cells = set([
            cell for cell in self._get_cells_with_potential_updates()
            if self._should_cell_be_alive_in_next_step(cell)
        ])

    def _get_cells_with_potential_updates(self):
        cells_with_potential_updates = set([])
        for live_cell in self._live_cells:
            cells_in_proximity = self._get_cells_in_proximity(
                live_cell
            )
            cells_with_potential_updates.update(cells_in_proximity)
        return cells_with_potential_updates

    def _should_cell_be_alive_in_next_step(self, cell):
        cells_in_proximity = self._get_cells_in_proximity(cell)
        live_cells_in_proximity = self._live_cells & cells_in_proximity

        len_of_live_cells_in_proximity = len(live_cells_in_proximity)
        if len_of_live_cells_in_proximity == 3:
            return True
        elif len_of_live_cells_in_proximity == 4:
            return cell in self._live_cells
        else:
            return False

    def _get_cells_in_proximity(self, (x, y)):
        cells_in_proximity = set([])

        for x_candidate in xrange(x - 1, x + 2):
            for y_candidate in xrange(y - 1, y + 2):
                if self._is_cell_in_bounds((x_candidate, y_candidate)):
                    cells_in_proximity.add((x_candidate, y_candidate))

        return cells_in_proximity


def print_function(string):
    """Function to print a string

    Args:
        string - string to print

    We need to this because in Python 2.7, `print` is a keyword and not a
    function so we can't pass it as an argument to functions.
    """
    print string


class BoardDrawer(object):
    """Responsible for drawing the board and printing it."""

    def __init__(self, print_function=print_function):
        """Constructs the `BoardDrawer` object.

        Keyword Args:
            print_function - injected depency describing a function that takes
                a string and prints it
        """
        self._print_function = print_function

    def draw(self, board):
        """Draws and prints a `board`

        Args:
            board - `Board` object to print

        Example:
        Given the board, Board(2, 2, live_cells=[(1, 1)]), prints the
        following:
        '''

        0 0
        0 1
        '''
        Notice that it prints an initial new line.
        """
        self._print_function('')
        for y in xrange(board.y_size):
            row = ' '.join(
                '1' if board[x, y] else '0' for x in xrange(board.x_size)
            )
            self._print_function(row)


if __name__ == '__main__':
    GameRunner().run()
