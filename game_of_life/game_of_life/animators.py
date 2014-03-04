"""`Animators` are responsible for animating a board and their steps.

`Animators` need to implement an `animate()` function that take a `Board`
object that represents the initial game board state.
"""
import curses
import time

from game_of_life.drawer import Drawer


class PrintAllAnimator(object):
    """`Animator` that prints an iteration of the `Board` one step at a time,
    onto the screen, sleeping for a short time in between printing.
    """

    _sleep_time = 1

    def __init__(self, drawer=None):
        """Creates the `PrintAllAnimator`

        Keyword Args:
           drawer - `Drawer` object that describes how each board will be drawn
        """
        self._drawer = drawer or Drawer()

    def animate(self, board):
        """Given a `Board` representing the initial game state, draws the
        progression of the board over time, separating the steps of the board
        by new lines. This never stops running.

        Args:
            board - `Board` to animate
        """
        while True:
            to_print = self._drawer.draw(board)
            to_print += '\n'
            print to_print
            board.step()
            time.sleep(self._sleep_time)


class CursesAnimator(object):
    """`Animator` that uses `curses`
    http://en.wikipedia.org/wiki/Curses_(programming_library), a terminal
    control library to animate the board.
    """

    def __init__(self, drawer=None):
        """Creates the `CursesAnimator`

        Keyword Args:
           drawer - `Drawer` object that describes how each board will be drawn
        """
        self._drawer = drawer or Drawer()

    def animate(self, board):
        """Animates the game board using curses to continually draw and refresh
        the screen. Finishes running when the user hits 'q'.
        """
        curses.wrapper(lambda _: self._run_curses(board))

    def _run_curses(self, board):
        screen = self._initialize_curses_screen()

        key_input = None
        iteration = 0

        # Continues to run until the user hits 'q'
        while key_input != ord('q'):
            self._draw_board_on_screen(screen, board, iteration)
            key_input = screen.getch()
            iteration += 1
            board.step()

        curses.endwin()

    def _initialize_curses_screen(self):
        screen = curses.initscr()
        screen.nodelay(1)
        screen.timeout(1000)
        return screen

    def _draw_board_on_screen(self, screen, board, iteration):
        screen.addstr(0, 0, 'Game Of Life')
        screen.addstr(1, 0, 'Welcome to the game of life! Hit q to quit')
        screen.addstr(3, 0, 'Iteration %i' % iteration)
        screen.addstr(4, 0, self._drawer.draw(board))
        screen.refresh()


def print_function(string):
    """Used as an injected dependency because in Python 2.7, `print` is a
    statement and not a function."""
    print string


class SingleFrameAnimator(object):
    """Animates a single frame at a particular step"""

    def __init__(
        self,
        step_to_animate,
        drawer=None,
        print_function=print_function
    ):
        """Creates a `SingleFrameAnimator` object
        Args:
            step_to_animate - the step that we want to animate
        """
        self._step_to_animate = step_to_animate
        self._drawer = drawer or Drawer()
        self._print_function = print_function

    def animate(self, board):
        """"""
        for _ in xrange(self._step_to_animate - 1):
            board.step()

        drawn_board = self._drawer.draw(board)
        self._print_function(drawn_board)
