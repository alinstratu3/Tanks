"""Generate readable arena palettes and contrasting player colors."""

from __future__ import annotations

from dataclasses import dataclass
import colorsys
import math
import random

from .config import PLAYER_ONE, PLAYER_TWO


Color = tuple[int, int, int]

TANK_COLOR_OPTIONS: tuple[Color, ...] = (
	PLAYER_ONE,
	PLAYER_TWO,
	(246, 201, 76),
	(142, 113, 242),
	(241, 109, 184),
	(112, 211, 78),
	(75, 153, 242),
	(242, 146, 57),
	(226, 82, 82),
	(79, 218, 220),
	(202, 108, 242),
	(215, 225, 77),
)


@dataclass(frozen=True)
class ArenaTheme:
	"""Colors used for the maze and both players in one match."""

	floor_a: Color
	floor_b: Color
	wall: Color
	wall_edge: Color
	grid_line: Color
	player_one: Color
	player_two: Color


def _hls_color(hue: float, lightness: float, saturation: float) -> Color:
	"""Convert normalized HLS values to an 8-bit RGB color."""
	red, green, blue = colorsys.hls_to_rgb(hue % 1.0, lightness, saturation)
	return round(red * 255), round(green * 255), round(blue * 255)


def _color_distance(first: Color, second: Color) -> float:
	return math.sqrt(sum((a - b) ** 2 for a, b in zip(first, second)))


def _contrasting_tank_colors(map_colors: tuple[Color, ...]) -> tuple[Color, Color]:
	"""Choose two distinct tank colors furthest from the current arena palette."""
	ranked_colors = sorted(
		TANK_COLOR_OPTIONS,
		key=lambda color: min(_color_distance(color, map_color) for map_color in map_colors),
		reverse=True,
	)
	player_one = ranked_colors[0]
	player_two = max(
		ranked_colors[1:],
		key=lambda color: min(
			_color_distance(color, map_color) for map_color in (*map_colors, player_one)
		),
	)
	return player_one, player_two


def make_random_theme(previous: ArenaTheme | None = None) -> ArenaTheme:
	"""Create a new map palette and tank colors that remain visually distinct."""
	for _ in range(32):
		hue = random.random()
		theme_hues = (
			hue,
			hue + 0.5 + random.uniform(-0.06, 0.06),
		)
		floor_hue, wall_hue = theme_hues
		floor_a = _hls_color(floor_hue, 0.22, 0.32)
		floor_b = _hls_color(floor_hue + 0.025, 0.27, 0.34)
		wall = _hls_color(wall_hue, 0.49, 0.34)
		wall_edge = _hls_color(wall_hue + 0.02, 0.61, 0.3)
		grid_line = _hls_color(floor_hue, 0.31, 0.28)
		map_colors = (floor_a, floor_b, wall, wall_edge, grid_line)
		player_one, player_two = _contrasting_tank_colors(map_colors)
		theme = ArenaTheme(
			floor_a,
			floor_b,
			wall,
			wall_edge,
			grid_line,
			player_one,
			player_two,
		)
		if previous is None or all(
			current != old
			for current, old in zip(
				map_colors,
				(
					previous.floor_a,
					previous.floor_b,
					previous.wall,
					previous.wall_edge,
					previous.grid_line,
				),
			)
		):
			return theme

	raise RuntimeError("Unable to generate a different arena theme.")
