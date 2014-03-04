import argparse

from game_of_life import animators
from game_of_life.loader import Loader
from game_of_life.loader import create_input_function_from_filename
from game_of_life.loader import parse_input


class GameOfLifeRunner(object):
    """Responsible for loading an initial game board and animating it."""

    def __init__(self, loader, animator):
        """Creates a `GameOfLifeRunner` object.

        Args:
            loader - a `Loader` object that is used to load a game board
            animator - an `Animator` object used to animate the loaded board
        """
        self._loader = loader
        self._animator = animator

    def run(self):
        """Handles loading the board and animating it"""
        board = self._loader.load()
        self._animator.animate(board)


class RunnerCreatorFromArgs(object):
    """Handles the creation of a `GameOfLifeRunner` object given the results of
    `argparse.ArgumentParser.parse_args()`, an `argparse.Namespace` object.
    """

    def __init__(self, args):
        """Creates a `RunnerCreatorFromArgs` object

        Args:
            args - a `argparse.Namespace` object that describes the command
                line arguments of the script
        """
        self._args = args

    def create(self):
        """Creates a `GameOfLifeRunner` object using the command line
        arguments.
        """
        loader = self._create_loader()
        animator = self._create_animator()
        return GameOfLifeRunner(loader, animator)

    def _create_loader(self):
        if self._args.filename:
            input_function = create_input_function_from_filename(
                self._args.filename
            )
        else:
            input_function = parse_input

        return Loader(input_function)

    def _create_animator(self):
        self._validate_animator_args()

        if self._args.step_to_print:
            return animators.SingleFrameAnimator(self._args.step_to_print)

        animator_name = self._args.animator or 'curses'
        animator_cls = self._animator_name_to_animator_cls_map[animator_name]
        return animator_cls()

    def _validate_animator_args(self):
        has_step_to_print = bool(self._args.step_to_print)
        has_animator = bool(self._args.animator)

        if not (has_step_to_print or has_animator):
            return

        if not (has_step_to_print ^ has_animator):
            raise argparse.ArgumentTypeError(
                'Cant have both --step-to-print and --animator options.'
            )

        if self._args.animator not in self._animator_name_to_animator_cls_map:
            raise argparse.ArgumentTypeError(
                'Invalid --animator. Must be one of %s' %
                self._animator_name_to_animator_cls_map.keys()
            )

    _animator_name_to_animator_cls_map = {
        'curses': animators.CursesAnimator,
        'print_all': animators.PrintAllAnimator
    }


def parse_args():
    parser = argparse.ArgumentParser(
        usage=""" %(prog)s [options].

If "--filename" is NOT passed in, the user can type in the board they want to
test. Hit return twice to mark that the input board is complete. Boards should
look like:

0 0
0 1

where "0"s represent dead cells and "1"s represent live cells."""
    )
    parser.add_argument(
        '--animator',
        help="""How to animate the game of life. Acceptable ANIMATORS include:
        "curses", and "print_all". "curses" uses `curses`, a terminal control
        library for Unix-like systems to draw and refresh the screen.  Hitting
        "q" will quit out of the process. "print_all" prints each iteration,
        one at a time, blank line separated. "print_all" creates an animator
        that runs indefinitely so this process will need to be explicitly
        killed via ctrl-c. The default ANIMATOR is "curses". This can not be
        used together with "--step-to-print"""
    )
    parser.add_argument(
        '--filename',
        help="""If passed in takes a input file that describes the initial
        grid.  Grids look like "0", "1" with spaces representing different
        columns and new lines representing different rows. Please look at
        "boards/blinker.txt" to see an example of a valid board."""
    )
    parser.add_argument(
        '--step-to-print',
        type=int,
        help="""The step to print. The initial step is step 1. This can not be
        used together with "--animator".
        """
    )
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    creator = RunnerCreatorFromArgs(args)
    runner = creator.create()
    runner.run()
