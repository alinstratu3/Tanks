"""Pygame drawing for the arena and its heads-up display."""

from __future__ import annotations

import pygame

from entities import Bullet, Tank
from game_config import (
	ARENA_X,
	ARENA_Y,
	BACKGROUND,
	FLOOR_A,
	FLOOR_B,
	FLAG_COLOR,
	GRID_HEIGHT,
	GRID_WIDTH,
	INK,
	MUTED,
	PANEL,
	SCREEN_HEIGHT,
	SCREEN_WIDTH,
	TILE_SIZE,
	WALL,
	WALL_EDGE,
)


class GameRenderer:
	def __init__(self) -> None:
		self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
		pygame.display.set_caption("Tanks | Labyrinth Run")
		self.title_font = pygame.font.SysFont("segoeui", 28, bold=True)
		self.body_font = pygame.font.SysFont("segoeui", 16)
		self.small_font = pygame.font.SysFont("segoeui", 13)

	def draw_tank(self, tank: Tank) -> None:
		x, y = round(tank.x), round(tank.y)
		dx, dy = tank.facing
		right_x, right_y = -dy, dx

		def point(forward: float, side: float, shadow: bool = False) -> tuple[int, int]:
			offset = 2 if shadow else 0
			return (
				round(x + dx * forward + right_x * side + offset),
				round(y + dy * forward + right_y * side + offset),
			)

		track_shape = (
			(-16, -15),
			(13, -15),
			(16, -12),
			(16, -9),
			(13, -7),
			(-16, -7),
			(-18, -10),
			(-18, -12),
		)
		for side in (-1, 1):
			track_points = [point(forward, lateral * side) for forward, lateral in track_shape]
			shadow_points = [
				point(forward, lateral * side, shadow=True)
				for forward, lateral in track_shape
			]
			pygame.draw.polygon(self.screen, (14, 19, 22), shadow_points)
			pygame.draw.polygon(self.screen, (35, 41, 41), track_points)
			pygame.draw.polygon(self.screen, (105, 117, 108), track_points, 1)
			for tread in (-13, -7, -1, 5, 11):
				pygame.draw.line(
					self.screen,
					(91, 102, 95),
					point(tread, 8 * side),
					point(tread, 14 * side),
					1,
				)

		hull_shape = (
			(15, 0),
			(10, -8),
			(-11, -8),
			(-15, -5),
			(-15, 5),
			(-11, 8),
			(10, 8),
		)
		pygame.draw.polygon(
			self.screen,
			(14, 19, 22),
			[point(forward, side, shadow=True) for forward, side in hull_shape],
		)
		hull_points = [point(forward, side) for forward, side in hull_shape]
		pygame.draw.polygon(self.screen, tank.color, hull_points)
		pygame.draw.polygon(self.screen, INK, hull_points, 1)
		pygame.draw.line(self.screen, (255, 255, 235), point(8, -6), point(-9, -6), 1)

		barrel_start = point(4, 0)
		barrel_end = point(23, 0)
		pygame.draw.line(self.screen, (21, 27, 29), barrel_start, barrel_end, 7)
		pygame.draw.line(self.screen, (176, 184, 164), barrel_start, barrel_end, 3)

		turret_shape = (
			(-6, -7),
			(4, -7),
			(9, -4),
			(9, 4),
			(4, 7),
			(-6, 7),
			(-10, 4),
			(-10, -4),
		)
		turret_points = [point(forward, side) for forward, side in turret_shape]
		pygame.draw.polygon(self.screen, (24, 32, 34), turret_points)
		pygame.draw.polygon(self.screen, tank.color, turret_points, 2)
		pygame.draw.circle(self.screen, (24, 32, 34), point(-2, 0), 4)
		pygame.draw.circle(self.screen, (175, 187, 169), point(-2, 0), 4, 1)

	def draw(
		self,
		players: list[Tank],
		walls: set[tuple[int, int]],
		bullets: list[Bullet],
		flag: tuple[float, float],
		notice: str,
		notice_timer: float,
		game_over: bool,
		winner_message: str,
	) -> None:
		self.screen.fill(BACKGROUND)
		pygame.draw.rect(self.screen, PANEL, (0, 0, SCREEN_WIDTH, 96))
		title = self.title_font.render("TANKS  /  LABYRINTH RUN", True, INK)
		self.screen.blit(title, (42, 22))
		level_label = self.body_font.render(
			"RANDOM ARENA     //     FIRST TO 3 CAPTURES WINS",
			True,
			MUTED,
		)
		self.screen.blit(level_label, (44, 60))

		for tank, x in zip(players, (630, 815)):
			pygame.draw.circle(self.screen, tank.color, (x, 35), 6)
			label = self.small_font.render(tank.name, True, MUTED)
			self.screen.blit(label, (x + 14, 27))
			score_label = self.body_font.render(f"{tank.score:02}", True, tank.color)
			self.screen.blit(score_label, (x + 142, 25))
			control = "WASD + SPACE" if tank is players[0] else "ARROWS + ENTER"
			control_label = self.small_font.render(control, True, INK)
			self.screen.blit(control_label, (x + 14, 48))

		for row in range(GRID_HEIGHT):
			for column in range(GRID_WIDTH):
				rectangle = pygame.Rect(
					ARENA_X + column * TILE_SIZE,
					ARENA_Y + row * TILE_SIZE,
					TILE_SIZE,
					TILE_SIZE,
				)
				if (column, row) in walls:
					pygame.draw.rect(self.screen, WALL, rectangle)
					pygame.draw.rect(self.screen, WALL_EDGE, rectangle, 1)
					pygame.draw.line(
						self.screen,
						(128, 146, 137),
						rectangle.topleft,
						(rectangle.right, rectangle.top),
						2,
					)
				else:
					floor = FLOOR_A if (column + row) % 2 else FLOOR_B
					pygame.draw.rect(self.screen, floor, rectangle)
					pygame.draw.rect(self.screen, (45, 59, 60), rectangle, 1)

		if not game_over:
			flag_x, flag_y = map(round, flag)
			pygame.draw.circle(self.screen, (87, 72, 41), (flag_x, flag_y), 20)
			pygame.draw.line(self.screen, FLAG_COLOR, (flag_x - 8, flag_y + 12), (flag_x - 8, flag_y - 14), 3)
			pygame.draw.polygon(
				self.screen,
				FLAG_COLOR,
				[(flag_x - 6, flag_y - 13), (flag_x + 12, flag_y - 8), (flag_x - 6, flag_y - 2)],
			)

			for bullet in bullets:
				pygame.draw.circle(
					self.screen,
					bullet.owner.color,
					(round(bullet.x), round(bullet.y)),
					bullet.radius + 2,
				)
				pygame.draw.circle(self.screen, INK, (round(bullet.x), round(bullet.y)), bullet.radius)
			for tank in players:
				self.draw_tank(tank)
		else:
			arena = pygame.Rect(
				ARENA_X,
				ARENA_Y,
				GRID_WIDTH * TILE_SIZE,
				GRID_HEIGHT * TILE_SIZE,
			)
			overlay = pygame.Surface(arena.size, pygame.SRCALPHA)
			overlay.fill((17, 24, 31, 190))
			self.screen.blit(overlay, arena.topleft)
			winner_label = self.title_font.render(winner_message, True, INK)
			self.screen.blit(winner_label, winner_label.get_rect(center=arena.center))

		footer_y = ARENA_Y + GRID_HEIGHT * TILE_SIZE + 18
		pygame.draw.line(
			self.screen,
			(55, 69, 72),
			(ARENA_X, footer_y),
			(ARENA_X + GRID_WIDTH * TILE_SIZE, footer_y),
		)
		if game_over:
			footer_message = self.small_font.render("R: NEW MATCH", True, MUTED)
		elif notice_timer > 0:
			footer_message = self.body_font.render(notice, True, INK)
		else:
			footer_message = self.small_font.render("R: NEW MATCH", True, MUTED)
		self.screen.blit(footer_message, (ARENA_X, footer_y + 12))
		pygame.display.flip()
