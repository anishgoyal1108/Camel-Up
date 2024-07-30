from gamemanager import GameManager
import unittest


class TestGameScore(unittest.TestCase):
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

class TestInitCamels(unittest.TestCase):
    def setUp(self) -> None:
        self.game_manager = GameManager()

    def test_0(self):
        """Test that the initiallized board is not blank"""
        self.game_manager.init_camels()
        blank_arr = [[] for _ in range(16)]
        self.assertTrue(self.game_manager.board != blank_arr)

class TestMoveCamels(unittest.TestCase):
    def setUp(self) -> None:
        self.game_manager = GameManager()

    def test_0(self):
        """Test that the board changes after a roll is not blank"""
        self.game_manager.init_camels()
        self.game_manager.move_camels("red", 3)
        blank_arr = [[] for _ in range(16)]
        self.assertTrue(self.game_manager.board != blank_arr)

if __name__ == "__main__":
    unittest.main()
