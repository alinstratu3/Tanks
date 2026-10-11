"""Game entities shared by simulation and rendering."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Tank:
	"""A player vehicle, including its controls and match score."""

	name: str
	color: tuple[int, int, int]
	spawn: tuple[float, float]
	controls: tuple[int, int, int, int]
	shoot_key: int
	score: int = 0
	x: float = 0
	y: float = 0
	facing: tuple[float, float] = (1, 0)
	cooldown: float = 0
	radius: int = 15

	def __post_init__(self) -> None:
		self.respawn()

	def respawn(self) -> None:
		"""Return to the spawn point without resetting the match score."""
		self.x, self.y = self.spawn
		self.cooldown = 0


@dataclass
class Bullet:
	"""A projectile tied to the tank that fired it."""

	x: float
	y: float
	vx: float
	vy: float
	owner: Tank
	radius: int = 5
