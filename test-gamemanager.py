from gamemanager import GameManager
import unittest


class TestGameManager(unittest.TestCase):
    def setUp(self) -> None:
        self.game_manager = GameManager()
        print(self.game_manager.dice)

    def update_score(self):
        self.game_manager.update_score
        self.assertNotEqual(self.game_manager.player_scores[0], 0)

    """def test_add_card(self):
        self.game_manager.add_card("red", 5)
        self.assertEqual(self.game_manager.cards["red"], [5])
        self.game_manager.add_card("red", 5)
        self.assertEqual(self.game_manager.cards["red"], [5, 3])

    def test_remove_card(self):
        self.game_manager.add_card("red", 5)
        self.game_manager.remove_card("red", 3)
        self.assertEqual(self.game_manager.cards["red"], [5])"""


if __name__ == "__main__":
    unittest.main()
