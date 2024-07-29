from gamemanager import GameManager
import unittest


class TestGameManager(unittest.TestCase):
    def setUp(self) -> None:
        self.game_manager = GameManager()
        self.game_manager.winning_camel = "red"
        self.game_manager.second_camel = "green"

    def test_0(self):
        self.game_manager.players[0].cards["red"] = [5]
        self.game_manager.update_score()
        self.assertEqual(self.game_manager.player_scores[0], 5)

    def test_1(self):
        self.game_manager.players[0].cards["red"] = []
        self.game_manager.players[0].cards["green"] = [5]
        self.game_manager.update_score()
        self.assertEqual(self.game_manager.player_scores[0], 1)

    """def test_1(self):
        self.game_manager.add_card("red", 5)
        self.assertEqual(self.game_manager.cards["red"], [5])
        self.game_manager.add_card("red", 5)
        self.assertEqual(self.game_manager.cards["red"], [5, 3])

    def test_2(self):
        self.game_manager.add_card("red", 5)
        self.game_manager.remove_card("red", 3)
        self.assertEqual(self.game_manager.cards["red"], [5])"""


if __name__ == "__main__":
    unittest.main()
