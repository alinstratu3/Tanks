"""Game state, input handling, and simulation loop."""

from __future__ import annotations

import math
import random
import sys

import pygame

from .config import (
	ARENA_X,
	ARENA_Y,
	FPS,
	GRID_HEIGHT,
	GRID_WIDTH,
	PLAYER_ONE,
	PLAYER_TWO,
	TILE_SIZE,
	WINNING_SCORE,
)
from .entities import Bullet, Tank
from .level import cell_center, make_random_walls
from .renderer import GameRenderer
from .theme import make_random_theme


class TanksGame:
	"""Own the match state and coordinate input, simulation, and rendering."""

	def __init__(self) -> None:
		pygame.init()
		self.renderer = GameRenderer()
		self.screen = self.renderer.screen
		self.clock = pygame.time.Clock()
		self.walls = make_random_walls()
		self.theme = make_random_theme()
		self.players = [
			Tank(
				"PLAYER 1",
				PLAYER_ONE,
				cell_center(1, 1),
				(pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d),
				pygame.K_SPACE,
			),
			Tank(
				"PLAYER 2",
				PLAYER_TWO,
				cell_center(14, 10),
				(pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT),
				pygame.K_RETURN,
			),
		]
		self._apply_tank_colors()
		self.flag = (-1, -1)
		self.relocate_flag()
		self.bullets: list[Bullet] = []
		self.game_over = False
		self.winner_message = ""
		self.notice = "Both tanks: reach the flag. A hit sends your rival back to spawn."
		self.notice_timer = 4.0

	def relocate_flag(self) -> None:
		"""Choose an open tile away from the spawns and, when possible, both tanks."""
		previous_flag = self.flag
		spawn_points = {tank.spawn for tank in self.players}
		candidates = [
			cell_center(column, row)
			for row in range(1, GRID_HEIGHT - 1)
			for column in range(1, GRID_WIDTH - 1)
			if (column, row) not in self.walls
			and cell_center(column, row) not in spawn_points
			and cell_center(column, row) != previous_flag
			and all(
				math.hypot(cell_center(column, row)[0] - tank.x, cell_center(column, row)[1] - tank.y)
				>= TILE_SIZE * 2
				for tank in self.players
			)
		]
		if not candidates:
			candidates = [
				cell_center(column, row)
				for row in range(1, GRID_HEIGHT - 1)
				for column in range(1, GRID_WIDTH - 1)
				if (column, row) not in self.walls
				and cell_center(column, row) not in spawn_points
				and cell_center(column, row) != previous_flag
			]
		self.flag = random.choice(candidates)

	def wall_at(self, x: float, y: float, radius: int) -> bool:
		"""Return whether a circular collision body overlaps any wall tile."""
		left = math.floor((x - radius - ARENA_X) / TILE_SIZE)
		right = math.floor((x + radius - ARENA_X) / TILE_SIZE)
		top = math.floor((y - radius - ARENA_Y) / TILE_SIZE)
		bottom = math.floor((y + radius - ARENA_Y) / TILE_SIZE)
		for column in range(left, right + 1):
			for row in range(top, bottom + 1):
				if (column, row) not in self.walls:
					continue
				rectangle = pygame.Rect(
					ARENA_X + column * TILE_SIZE,
					ARENA_Y + row * TILE_SIZE,
					TILE_SIZE,
					TILE_SIZE,
				)
				closest_x = max(rectangle.left, min(x, rectangle.right))
				closest_y = max(rectangle.top, min(y, rectangle.bottom))
				if (x - closest_x) ** 2 + (y - closest_y) ** 2 < radius**2:
					return True
		return False

	def move_tank(self, tank: Tank, keys: pygame.key.ScancodeWrapper, dt: float) -> None:
		up, down, left, right = tank.controls
		dx = float(keys[right]) - float(keys[left])
		dy = float(keys[down]) - float(keys[up])
		length = math.hypot(dx, dy)
		if length == 0:
			return
		# Normalize diagonals so they do not move faster than cardinal input.
		dx, dy = dx / length, dy / length
		tank.facing = (dx, dy)
		speed = 170 * dt
		next_x = tank.x + dx * speed
		if not self.wall_at(next_x, tank.y, tank.radius):
			tank.x = next_x
		next_y = tank.y + dy * speed
		if not self.wall_at(tank.x, next_y, tank.radius):
			tank.y = next_y

	def fire(self, tank: Tank) -> None:
		if tank.cooldown > 0:
			return
		direction_x, direction_y = tank.facing
		self.bullets.append(
			Bullet(
				tank.x + direction_x * 22,
				tank.y + direction_y * 22,
				direction_x * 390,
				direction_y * 390,
				tank,
			)
		)
		tank.cooldown = 0.42

	def update(self, dt: float) -> None:
		"""Advance one simulation step; dt is capped by the outer game loop."""
		if self.game_over:
			return
		keys = pygame.key.get_pressed()
		for tank in self.players:
			tank.cooldown = max(0, tank.cooldown - dt)
			self.move_tank(tank, keys, dt)

		for bullet in self.bullets[:]:
			bullet.x += bullet.vx * dt
			bullet.y += bullet.vy * dt
			if self.wall_at(bullet.x, bullet.y, bullet.radius):
				self.bullets.remove(bullet)
				continue
			target = next(player for player in self.players if player is not bullet.owner)
			if math.hypot(bullet.x - target.x, bullet.y - target.y) < target.radius + bullet.radius:
				target.respawn()
				self.bullets.remove(bullet)
				self.notice = f"{target.name} hit! Back to the starting tile."
				self.notice_timer = 2.0

		for tank in self.players:
			if math.hypot(tank.x - self.flag[0], tank.y - self.flag[1]) < 25:
				tank.score += 1
				if tank.score >= WINNING_SCORE:
					self.game_over = True
					self.bullets.clear()
					player_number = self.players.index(tank) + 1
					self.winner_message = f"Player {player_number} won"
					self.notice = self.winner_message
				else:
					self.relocate_flag()
					self.notice = f"{tank.name} captured the flag! Score: {tank.score}."
				self.notice_timer = 2.0
				break
		self.notice_timer = max(0, self.notice_timer - dt)

	def handle_event(self, event: pygame.event.Event) -> None:
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type != pygame.KEYDOWN:
			return
		if event.key == pygame.K_ESCAPE:
			pygame.quit()
			sys.exit()
		if event.key == pygame.K_r:
			self.reset()
			return
		if self.game_over:
			return
		for tank in self.players:
			if event.key == tank.shoot_key:
				self.fire(tank)

	def reset(self) -> None:
		"""Start a fresh match and generate a new random maze."""
		for tank in self.players:
			tank.respawn()
			tank.score = 0
		self.walls = make_random_walls()
		self.theme = make_random_theme(self.theme)
		self._apply_tank_colors()
		self.bullets.clear()
		self.game_over = False
		self.winner_message = ""
		self.flag = (-1, -1)
		self.relocate_flag()
		self.notice = "Both tanks: reach the flag. A hit sends your rival back to spawn."
		self.notice_timer = 3.0

	def _apply_tank_colors(self) -> None:
		"""Match each tank's UI and sprite color to the active arena palette."""
		self.players[0].color = self.theme.player_one
		self.players[1].color = self.theme.player_two

	def draw(self) -> None:
		self.renderer.draw(
			self.players,
			self.walls,
			self.bullets,
			self.flag,
			self.notice,
			self.notice_timer,
			self.game_over,
			self.winner_message,
			self.theme,
		)

	def run(self) -> None:
		while True:
			dt = min(self.clock.tick(FPS) / 1000, 0.05)
			for event in pygame.event.get():
				self.handle_event(event)
			self.update(dt)
			self.draw()
