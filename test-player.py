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

class TestPlayerBet(unittest.TestCase):
    def setUp(self) -> None:
        self.player = Player()
        self.cards = {
            "red": [5, 3, 2, 2],
            "green": [5, 3, 2, 2],
            "blue": [5, 3, 2, 2],
            "yellow": [5, 3, 2, 2],
            "purple": [5, 3, 2, 2],
        }

    def test_0(self):
        """Test return datatype"""
        color = "red"
        actual = self.player.take_bet(color, self.cards)
        self.assertIsInstance(actual, dict)
    
    def test_1(self):
        """Take 1 card"""
        color = "red"
        newDict = self.player.take_bet(color, self.cards)
        actual = newDict[color]
        self.assertListEqual(actual, [3, 2, 2])
    
    def test_2(self):
        """Take 2 cards"""
        color = "red"
        newDict = self.player.take_bet(color, self.cards)
        self.cards = newDict
        newDict = self.player.take_bet(color, self.cards)
        actual = newDict[color]
        self.assertListEqual(actual, [2, 2])


if __name__ == "__main__":
    unittest.main()
