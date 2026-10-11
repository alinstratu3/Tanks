"""Tests for match completion and restart behavior."""

from __future__ import annotations

import os
import unittest
from unittest.mock import patch

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import pygame

from tanksgame.config import WINNING_SCORE
from tanksgame.game import TanksGame
from tanksgame.theme import make_random_theme


class MatchRuleTests(unittest.TestCase):
	def setUp(self) -> None:
		pygame.init()
		self.game = TanksGame()

	def tearDown(self) -> None:
		pygame.quit()

	def test_each_player_wins_at_three_captures(self) -> None:
		for player_number, winner in enumerate(self.game.players, start=1):
			with self.subTest(player_number=player_number):
				self.game.reset()
				winner.score = WINNING_SCORE - 1
				winner.x, winner.y = self.game.flag

				self.game.update(1 / 60)

				self.assertTrue(self.game.game_over)
				self.assertEqual(self.game.winner_message, f"Player {player_number} won")
				self.assertEqual(winner.score, WINNING_SCORE)

	def test_restart_generates_a_new_maze_and_clears_winner(self) -> None:
		fresh_maze = {(0, 0), (1, 0), (2, 0)}
		previous_theme = self.game.theme
		fresh_theme = make_random_theme(self.game.theme)
		with patch("tanksgame.game.make_random_walls", return_value=fresh_maze) as generator:
			with patch("tanksgame.game.make_random_theme", return_value=fresh_theme) as theme_generator:
				self.game.game_over = True
				self.game.winner_message = "Player 1 won"
				self.game.reset()

		generator.assert_called_once_with()
		theme_generator.assert_called_once_with(previous_theme)
		self.assertEqual(self.game.walls, fresh_maze)
		self.assertEqual(self.game.theme, fresh_theme)
		self.assertFalse(self.game.game_over)
		self.assertEqual(self.game.winner_message, "")
		self.assertTrue(all(player.score == 0 for player in self.game.players))
		self.assertEqual(
			[player.color for player in self.game.players],
			[fresh_theme.player_one, fresh_theme.player_two],
		)


if __name__ == "__main__":
	unittest.main()
