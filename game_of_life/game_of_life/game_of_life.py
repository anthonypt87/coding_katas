class GameOfLife(object):
    """Responsible for loading an initial game board and animating it."""

    def __init__(self, loader, animator):
        """Creates a `GameOfLife` object.

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
