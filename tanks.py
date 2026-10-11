"""Source-checkout launcher and compatibility exports."""

from __future__ import annotations

import sys
from pathlib import Path

# Make the src-layout package importable when running this file directly.
SOURCE_DIRECTORY = Path(__file__).parent / "src"
sys.path.insert(0, str(SOURCE_DIRECTORY))

from tanksgame import (  # noqa: E402
	Bullet,
	Tank,
	TanksGame,
	cell_center,
	make_level_one_walls,
	make_random_walls,
)
from tanksgame.config import (  # noqa: E402
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
