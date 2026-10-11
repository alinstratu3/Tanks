"""Tests for generated maze invariants."""

from __future__ import annotations

import unittest

from tanksgame.config import GRID_HEIGHT, GRID_WIDTH
from tanksgame.level import make_random_walls


class RandomMazeTests(unittest.TestCase):
	def test_maze_has_solid_border_and_open_spawns(self) -> None:
		walls = make_random_walls()
		border = {
			(column, row)
			for column in range(GRID_WIDTH)
			for row in range(GRID_HEIGHT)
			if column in (0, GRID_WIDTH - 1) or row in (0, GRID_HEIGHT - 1)
		}
		spawn_areas = {
			(spawn_column + dx, spawn_row + dy)
			for spawn_column, spawn_row in ((1, 1), (GRID_WIDTH - 2, GRID_HEIGHT - 2))
			for dx in (-1, 0, 1)
			for dy in (-1, 0, 1)
		}

		self.assertTrue(border.issubset(walls))
		self.assertFalse((spawn_areas - border) & walls)

	def test_all_walkable_tiles_are_connected(self) -> None:
		walls = make_random_walls()
		floor = {
			(column, row)
			for column in range(1, GRID_WIDTH - 1)
			for row in range(1, GRID_HEIGHT - 1)
			if (column, row) not in walls
		}
		reached = {next(iter(floor))}
		frontier = list(reached)

		while frontier:
			column, row = frontier.pop()
			for neighbor in (
				(column - 1, row),
				(column + 1, row),
				(column, row - 1),
				(column, row + 1),
			):
				if neighbor in floor and neighbor not in reached:
					reached.add(neighbor)
					frontier.append(neighbor)

		self.assertEqual(reached, floor)


if __name__ == "__main__":
	unittest.main()
