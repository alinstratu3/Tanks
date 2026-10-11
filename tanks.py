"""Compatibility entry point for the Tanks game."""

from entities import Bullet, Tank
from game import TanksGame
from game_config import (
	ARENA_X,
	ARENA_Y,
	BACKGROUND,
	FLOOR_A,
	FLOOR_B,
	FPS,
	FLAG_COLOR,
	GRID_HEIGHT,
	GRID_WIDTH,
	INK,
	MUTED,
	PANEL,
	PLAYER_ONE,
	PLAYER_TWO,
	SCREEN_HEIGHT,
	SCREEN_WIDTH,
	TILE_SIZE,
	WALL,
	WALL_EDGE,
	WINNING_SCORE,
)
from level import cell_center, make_level_one_walls, make_random_walls

__all__ = [
	"ARENA_X",
	"ARENA_Y",
	"BACKGROUND",
	"Bullet",
	"FLOOR_A",
	"FLOOR_B",
	"FPS",
	"FLAG_COLOR",
	"GRID_HEIGHT",
	"GRID_WIDTH",
	"INK",
	"MUTED",
	"PANEL",
	"PLAYER_ONE",
	"PLAYER_TWO",
	"SCREEN_HEIGHT",
	"SCREEN_WIDTH",
	"TILE_SIZE",
	"Tank",
	"TanksGame",
	"WALL",
	"WALL_EDGE",
	"WINNING_SCORE",
	"cell_center",
	"make_level_one_walls",
	"make_random_walls",
]


if __name__ == "__main__":
	TanksGame().run()
