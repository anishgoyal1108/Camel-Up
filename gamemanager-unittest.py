from gamemanager import GameManager
import unittest


class TestGameManager(unittest.TestCase):
    def setUp(self):
        self.game_manager = GameManager()

    def update_score(self, score):
        self.game_manager.score += score
        self.assertEqual(self.game_manager.score, score)

    def test_update_score(self):
        self.update_score(10)
        self.update_score(-5)
        self.update_score(0)
        self.update_score(20)

    def test_add_card(self):
        self.game_manager.add_card("red", 5)
        self.assertEqual(self.game_manager.cards["red"], [5])
        self.game_manager.add_card("red", 5)
        self.assertEqual(self.game_manager.cards["red"], [5, 3])

    def test_remove_card(self):
        self.game_manager.add_card("red", 5)
        self.game_manager.remove_card("red", 3)
        self.assertEqual(self.game_manager.cards["red"], [5])


if __name__ == "__main__":
    unittest.main()
