"""Maze layout and arena coordinate helpers."""

import random

from .config import ARENA_X, ARENA_Y, GRID_HEIGHT, GRID_WIDTH, TILE_SIZE


def cell_center(column: int, row: int) -> tuple[float, float]:
	return (
		ARENA_X + column * TILE_SIZE + TILE_SIZE / 2,
		ARENA_Y + row * TILE_SIZE + TILE_SIZE / 2,
	)


def make_level_one_walls() -> set[tuple[int, int]]:
	"""Build the original handcrafted maze, retained for compatibility."""
	walls = {
		(column, row)
		for column in range(GRID_WIDTH)
		for row in range(GRID_HEIGHT)
		if column in (0, GRID_WIDTH - 1) or row in (0, GRID_HEIGHT - 1)
	}

	def add_vertical(column: int, start: int, end: int) -> None:
		walls.update((column, row) for row in range(start, end + 1))

	def add_horizontal(row: int, start: int, end: int) -> None:
		walls.update((column, row) for column in range(start, end + 1))

	add_vertical(4, 1, 3)
	add_vertical(4, 6, 9)
	add_vertical(8, 2, 6)
	add_vertical(8, 8, 10)
	add_vertical(12, 1, 4)
	add_vertical(12, 6, 10)
	for start, end in ((1, 2), (5, 7), (9, 11)):
		add_horizontal(4, start, end)
	for start, end in ((1, 3), (5, 6), (9, 10), (13, 13)):
		add_horizontal(8, start, end)
	add_horizontal(2, 6, 7)
	add_horizontal(6, 1, 2)
	add_horizontal(6, 5, 6)
	add_horizontal(6, 10, 11)
	return walls


def make_random_walls() -> set[tuple[int, int]]:
	"""Generate connected random obstacles with clear spawn areas."""
	walls = {
		(column, row)
		for column in range(GRID_WIDTH)
		for row in range(GRID_HEIGHT)
		if column in (0, GRID_WIDTH - 1) or row in (0, GRID_HEIGHT - 1)
	}
	spawn_clearance = {
		(spawn_column + column_offset, spawn_row + row_offset)
		for spawn_column, spawn_row in ((1, 1), (GRID_WIDTH - 2, GRID_HEIGHT - 2))
		for column_offset in (-1, 0, 1)
		for row_offset in (-1, 0, 1)
	}
	candidates = [
		(column, row)
		for row in range(1, GRID_HEIGHT - 1)
		for column in range(1, GRID_WIDTH - 1)
		if (column, row) not in spawn_clearance
	]
	random.shuffle(candidates)
	target_walls = random.randint(18, 24)
	obstacle_count = 0

	def has_connected_floor() -> bool:
		# A connectivity check keeps every generated tile reachable from every other.
		floor_cells = {
			(column, row)
			for row in range(1, GRID_HEIGHT - 1)
			for column in range(1, GRID_WIDTH - 1)
			if (column, row) not in walls
		}
		start = next(iter(floor_cells))
		reached = {start}
		frontier = [start]
		while frontier:
			column, row = frontier.pop()
			for neighbor in (
				(column - 1, row),
				(column + 1, row),
				(column, row - 1),
				(column, row + 1),
			):
				if neighbor in floor_cells and neighbor not in reached:
					reached.add(neighbor)
					frontier.append(neighbor)
		return reached == floor_cells

	for cell in candidates:
		walls.add(cell)
		if not has_connected_floor():
			walls.remove(cell)
			continue
		obstacle_count += 1
		if obstacle_count >= target_walls:
			break

	return walls
