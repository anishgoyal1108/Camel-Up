import unittest
from evbot import EVBot
from gamemanager import GameManager

class TestSimulateMove(unittest.TestCase):
    def setUp(self) -> None:
        self.game = GameManager().init_camels()
        self.bot = EVBot(self.game)

    def test_0(self):
        """Test return datatype"""
        actual = self.bot.simulate_move("red", 1, self.game.board)
        self.assertIsInstance(actual, tuple[list[list], str, str])

if __name__ == "__main__":
    unittest.main()
