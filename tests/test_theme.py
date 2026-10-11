"""Tests for random map colors and tank contrast."""

from __future__ import annotations

import unittest

from tanksgame.theme import ArenaTheme, make_random_theme


def color_distance(first: tuple[int, int, int], second: tuple[int, int, int]) -> float:
	return sum((a - b) ** 2 for a, b in zip(first, second)) ** 0.5


class ArenaThemeTests(unittest.TestCase):
	def test_theme_changes_and_tanks_contrast_with_arena_colors(self) -> None:
		theme = make_random_theme()
		next_theme = make_random_theme(theme)
		map_colors = (
			next_theme.floor_a,
			next_theme.floor_b,
			next_theme.wall,
			next_theme.wall_edge,
			next_theme.grid_line,
		)

		self.assertNotEqual(theme, next_theme)
		for old_color, new_color in zip(
			(
				theme.floor_a,
				theme.floor_b,
				theme.wall,
				theme.wall_edge,
				theme.grid_line,
			),
			map_colors,
		):
			self.assertNotEqual(old_color, new_color)
		for tank_color in (next_theme.player_one, next_theme.player_two):
			self.assertGreater(
				min(color_distance(tank_color, map_color) for map_color in map_colors),
				100,
			)
		self.assertGreater(
			color_distance(next_theme.player_one, next_theme.player_two),
			100,
		)

	def test_previous_theme_type_is_supported(self) -> None:
		theme = make_random_theme()
		self.assertIsInstance(theme, ArenaTheme)
		self.assertIsInstance(make_random_theme(theme), ArenaTheme)


if __name__ == "__main__":
	unittest.main()
