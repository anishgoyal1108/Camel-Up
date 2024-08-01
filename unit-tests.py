import unittest
from gamemanager import GameManager
from evbot import EVBot
from player import Player
from playgame import PlayGame


# PLAYGAME UNIT TESTS
class TestPlayGame(unittest.TestCase):
    def test_0(self):
        """
        Test taking turns between two players. BETTING version.
        Tests the following simultaneously:
        - Starting with Player1
        - Changing the turn order
        - Betting on a specific color
        - Bets are stored properly for each player
        - Betted cards are removed from GameManager
        """
        game = PlayGame(GameManager(Player1=Player("Alice"), Player2=Player("Bob")))
        alice = game.manager.players[0]
        bob = game.manager.players[1]
        self.assertEqual(game.current_player.name, "Alice")
        game.take_turn("B", "red")
        self.assertEqual(game.current_player.name, "Bob")
        self.assertEqual(alice.cards["red"], [5])
        self.assertEqual(game.manager.cards["red"], [3, 2, 2])
        game.take_turn("B", "green")
        self.assertEqual(game.current_player.name, "Alice")
        self.assertEqual(bob.cards["green"], [5])
        self.assertEqual(game.manager.cards["green"], [3, 2, 2])
        game.take_turn("B", "red")
        self.assertEqual(game.current_player.name, "Bob")
        self.assertEqual(alice.cards["red"], [5, 3])
        self.assertEqual(game.manager.cards["red"], [2, 2])

    def test_1(self):
        """
        Test taking turns between two players. ROLL version.
        Tests the following simultaneously:
        - Starting with Player1
        - Changing the turn order
        - Rolling for a random color
        - Incrementing the coin count
        - Updating the dice state
        - Appending the dice count
        """
        game = PlayGame(GameManager(Player1=Player("Alice"), Player2=Player("Bob")))
        alice = game.manager.players[0]
        bob = game.manager.players[1]
        self.assertEqual(game.current_player.name, "Alice")
        game.take_turn("R")
        self.assertEqual(game.current_player.name, "Bob")
        self.assertEqual(alice.coins, 4)
        self.assertEqual(
            len([key for key in game.manager.dice if game.manager.dice[key] == 0]), 4
        )
        self.assertEqual(game.num_dice_rolled, 1)
        game.take_turn("R")
        self.assertEqual(game.current_player.name, "Alice")
        self.assertEqual(bob.coins, 4)
        self.assertEqual(
            len([key for key in game.manager.dice if game.manager.dice[key] == 0]), 3
        )
        self.assertEqual(game.num_dice_rolled, 2)

    def test_2(self):
        """
        Players cannot bet > 4 times on the same camel, or the program will
        encounter an IndexError.

        NOTE: This exception will never actually be thrown, since we check
        the length of the remaining betting cards before accepting the user's response.
        """
        game = PlayGame(GameManager(Player1=Player("Alice"), Player2=Player("Bob")))
        self.assertEqual(game.current_player.name, "Alice")
        game.take_turn("B", "red")
        self.assertEqual(game.current_player.name, "Bob")
        game.take_turn("B", "red")
        self.assertEqual(game.current_player.name, "Alice")
        game.take_turn("B", "red")
        self.assertEqual(game.current_player.name, "Bob")
        game.take_turn("B", "red")
        self.assertEqual(game.current_player.name, "Alice")
        with self.assertRaises(IndexError):
            game.take_turn("B", "red")

    def test_3(self):
        """
        Test getting hint for a player's turn.
        """
        pass

    def test_4(self):
        pass


# PLAYER UNIT TESTS
class TestPlayerRoll(unittest.TestCase):
    def setUp(self) -> None:
        self.player = Player("Alice")
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
        self.player = Player("Alice")
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


class TestPlayerHint(unittest.TestCase):
    def setUp(self) -> None:
        self.player = Player("Alice")
        pass


# EV BOT UNIT TESTS
class TestSimulateMove(unittest.TestCase):
    def setUp(self) -> None:
        self.game = GameManager().init_camels()
        self.bot = EVBot(self.game)

    def test_0(self):
        """Test return datatype"""
        actual = self.bot.simulate_move("red", 1, self.game.board)
        self.assertIsInstance(actual, tuple[list[list], str, str])


# GAMEMANAGER UNIT TESTS
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
