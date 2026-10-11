"""Allow launching the game with ``python -m tanksgame``."""

from .game import TanksGame


def main() -> None:
	"""Start a new game session."""
	TanksGame().run()


if __name__ == "__main__":
	main()
