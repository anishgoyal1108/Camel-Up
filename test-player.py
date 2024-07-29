import unittest
from player import Player


class TestPlayerRoll(unittest.TestCase):
    def setUp(self) -> None:
        self.player = Player()
        self.dice = ["red", "green", "blue", "yellow", "purple"]

    def test_0(self):
        """Test return datatype"""
        actual = self.player.roll(self.dice)
        self.assertIsInstance(actual, tuple)

    def test_1(self):
        """Roll is a number from 1 to 3 (inclusive)"""
        actual = self.player.roll(self.dice)
        self.assertIsInstance(actual[0], str)

    def test_2(self):
        """Roll is a number from 1 to 3 (inclusive)"""
        actual = self.player.roll(self.dice)
        self.assertIsInstance(actual[1], int)

    def test_3(self):
        """Roll is a number from 1 to 3 (inclusive)"""
        actual = self.player.roll(self.dice)
        self.assertTrue(1 <= actual[1] <= 3)


if __name__ == "__main__":
    unittest.main()
