from gamemanager import GameManager
import unittest


'''class TestGameScore(unittest.TestCase):
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
        self.assertTrue(self.game_manager.board != blank_arr)'''

class TestMoveCamels(unittest.TestCase):
    def setUp(self) -> None:
        self.game_manager = GameManager()

    def test_0(self):
        """Test that the board changes after a roll"""
        self.game_manager.board = [[] for _ in range(16)]
        self.game_manager.board[0].append("red")
        expected = [[], [], [], ["red"], [], [], [], [], [], [], [], [], [], [], [], []]
        self.game_manager.move_camels("red", 3)
        self.assertListEqual(self.game_manager.board, expected)
    
    def test_1(self):
        """Test that the red camel is in the right spot"""
        self.game_manager.board.clear()
        self.game_manager.board = [[] for _ in range(16)]
        self.game_manager.board[0].append("red")
        self.game_manager.move_camels("red", 3)
        actual = self.game_manager.board[3]
        self.assertTrue(actual == ["red"])
    
    def test_2(self):
        """Test that all the stacked camels are in the right spot"""
        self.game_manager.board.clear()
        self.game_manager.board = [[] for _ in range(16)]
        self.game_manager.board[0].append("red")
        self.game_manager.board[0].append("green")
        self.game_manager.move_camels("red", 3)
        actual = self.game_manager.board[3]
        self.assertTrue(actual == ["red", "green"])
    
    def test_3(self):
        """Test that the winning camel is initiallized when a camel passes the finish line"""
        self.game_manager.board.clear()
        self.game_manager.board = [[] for _ in range(16)]
        self.game_manager.board[14].append("red")
        self.game_manager.move_camels("red", 3)
        self.assertIsNotNone(self.game_manager.winning_camel)
    
    def test_4(self):
        """Test that the second camel is also initiallized when a camel passes the finish line"""
        self.game_manager.board.clear()
        self.game_manager.board = [[] for _ in range(16)]
        self.game_manager.board[14].append("red")
        self.game_manager.board[14].append("green")
        self.game_manager.move_camels("red", 3)
        self.assertIsNotNone(self.game_manager.second_camel)
    
    def test_5(self):
        """Test that the winning camel is the right one"""
        self.game_manager.board.clear()
        self.game_manager.board = [[] for _ in range(16)]
        self.game_manager.board[14].append("red")
        self.game_manager.move_camels("red", 3)
        self.assertEqual(self.game_manager.winning_camel, "red")
    
    def test_6(self):
        """Test that the second camel is the right one"""
        self.game_manager.board.clear()
        self.game_manager.board = [[] for _ in range(16)]
        self.game_manager.board[14].append("red")
        self.game_manager.board[14].append("green")
        self.game_manager.move_camels("red", 3)
        self.assertEqual(self.game_manager.second_camel, "red")
    
    def test_7(self):
        """Test that the function works when the second camel doesn't cross the finish line"""
        self.game_manager.board.clear()
        self.game_manager.board = [[] for _ in range(16)]
        self.game_manager.board[14].append("red")
        self.game_manager.board[10].append("green")
        self.game_manager.move_camels("red", 3)
        self.assertEqual(self.game_manager.second_camel, "green")

if __name__ == "__main__":
    unittest.main()
