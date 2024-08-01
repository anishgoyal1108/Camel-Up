import unittest
from gamemanager import GameManager
from evbot import EVBot
from player import Player
from playgame import PlayGame
from copy import deepcopy


class TestPlayGame(unittest.TestCase):
    """
    Unit test cases for the PlayGame class.
    """

    def setUp(self):
        self.game = PlayGame(GameManager(Player("Alice"), Player("Bob")))
        self.alice = self.game.manager.players[0]
        self.bob = self.game.manager.players[1]

    """
    Unit tests for these methods: 
    - PlayGame.take_turn
    - PlayGame.switch_turn
    - PlayGame.handle_bet
    - PlayGame.handle_roll
    """

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
        self.game.take_turn("B", "red")
        self.assertEqual(self.game.current_player.name, "Bob")
        self.assertEqual(self.alice.cards["red"], [5])
        self.assertEqual(self.game.manager.cards["red"], [3, 2, 2])
        self.game.take_turn("B", "green")
        self.assertEqual(self.game.current_player.name, "Alice")
        self.assertEqual(self.bob.cards["green"], [5])
        self.assertEqual(self.game.manager.cards["green"], [3, 2, 2])
        self.game.take_turn("B", "red")
        self.assertEqual(self.game.current_player.name, "Bob")
        self.assertEqual(self.alice.cards["red"], [5, 3])
        self.assertEqual(self.game.manager.cards["red"], [2, 2])

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
        self.assertEqual(self.game.current_player.name, "Alice")
        self.game.take_turn("R")
        self.assertEqual(self.game.current_player.name, "Bob")
        self.assertEqual(self.alice.coins, 4)
        self.assertEqual(
            len(
                [
                    key
                    for key in self.game.manager.dice
                    if self.game.manager.dice[key] == 0
                ]
            ),
            4,
        )
        self.assertEqual(self.game.num_dice_rolled, 1)
        self.game.take_turn("R")
        self.assertEqual(self.game.current_player.name, "Alice")
        self.assertEqual(self.bob.coins, 4)
        self.assertEqual(
            len(
                [
                    key
                    for key in self.game.manager.dice
                    if self.game.manager.dice[key] == 0
                ]
            ),
            3,
        )
        self.assertEqual(self.game.num_dice_rolled, 2)

    def test_2(self):
        """
        Players cannot bet > 4 times on the same camel, or the program will
        encounter an IndexError.

        NOTE: This exception will never actually be thrown, since we check
        the length of the remaining betting cards before accepting the user's
        response.
        """
        self.assertEqual(self.game.current_player.name, "Alice")
        self.game.take_turn("B", "red")
        self.assertEqual(self.game.current_player.name, "Bob")
        self.game.take_turn("B", "red")
        self.assertEqual(self.game.current_player.name, "Alice")
        self.game.take_turn("B", "red")
        self.assertEqual(self.game.current_player.name, "Bob")
        self.game.take_turn("B", "red")
        self.assertEqual(self.game.current_player.name, "Alice")
        with self.assertRaises(IndexError):
            self.game.take_turn("B", "red")

    """
    Test PlayGame.handle_hint
   
    NOTE: We only test coin decrementing functionality and turn 
    mechanics for now (we check EVBot later).
    """

    def test_3(self):
        """
        Test decrementing coins when hint is given.
        """
        self.alice.coins = 1
        self.game.handle_hint(skip_evbot=True)
        self.assertEqual(self.alice.coins, 0)

    def test_4(self):
        """
        Test turn handling with hints. The player who made the
        hint should still retain their turn.
        """
        self.game.take_turn(action="H", skip_evbot=True)
        self.assertEqual(self.game.current_player.name, "Alice")
        self.assertEqual(self.alice.coins, 2)


class TestPlayer(unittest.TestCase):
    """
    Unit test cases for the Player class.
    """

    def setUp(self) -> None:
        self.player = Player("Alice")
        self.dice = ["red", "green", "blue", "yellow", "purple"]
        self.game_cards = {
            "red": [5, 3, 2, 2],
            "green": [5, 3, 2, 2],
            "blue": [5, 3, 2, 2],
            "yellow": [5, 3, 2, 2],
            "purple": [5, 3, 2, 2],
        }
        self.roll_result = self.color, self.result = self.player.roll(self.dice)

    # Unit tests for Player.roll
    def test_0(self):
        """
        Test return datatype.
        """
        self.assertIsInstance(self.roll_result, tuple)
        self.assertIsInstance(self.color, str)
        self.assertIsInstance(self.result, int)

    def test_1(self):
        """
        Roll is a number from 1-3, inclusive.
        """
        self.assertTrue(1 <= self.result <= 3)
        self.assertEqual(self.player.coins, 4)

    def test_2(self):
        """
        Roll is a number from 1-3, inclusive.
        """
        self.assertTrue(1 <= self.result <= 3)
        self.assertEqual(self.player.coins, 4)

    def test_3(self):
        """
        Roll is a number from 1-3, inclusive.
        """
        self.assertTrue(1 <= self.result <= 3)
        self.assertEqual(self.player.coins, 4)

    def test_4(self):
        """
        Test multiple rolls.
        """
        for _ in range(100):
            og_amt = self.player.coins
            self.assertTrue(1 <= self.result <= 3)
            self.roll_result = self.color, self.result = self.player.roll(self.dice)
            self.assertEqual(og_amt + 1, self.player.coins)

    # Unit tests for Player.take_bet
    def test_5(self):
        """
        Test return datatype.
        """
        self.assertIsInstance(self.player.take_bet("red", self.game_cards), dict)

    def test_6(self):
        """
        Take the top red card.
        """
        self.assertListEqual(
            self.player.take_bet("red", self.game_cards)["red"], [3, 2, 2]
        )

    def test_7(self):
        """
        Take the top two red cards.
        """
        for _ in range(2):
            self.game_cards = self.player.take_bet("red", self.game_cards)
        self.assertListEqual(self.game_cards["red"], [2, 2])

    def test_8(self):
        """
        Take all four red cards.
        """
        for _ in range(4):
            self.game_cards = self.player.take_bet("red", self.game_cards)
        self.assertListEqual(self.game_cards["red"], [])

    def test_9(self):
        """
        Take all cards from all colors.
        """
        for color in self.game_cards:
            for _ in range(4):
                self.game_cards = self.player.take_bet(color, self.game_cards)
            self.assertListEqual(self.game_cards[color], [])


class TestEVBot(unittest.TestCase):
    """
    Unit test cases for the EVBot class.
    """

    def setUp(self) -> None:
        self.game = GameManager(Player("Alice"), Player("Bob"))
        self.game.init_camels()
        self.bot = EVBot(self.game)

    # Test EVBot.simulate_move
    def test_0(self):
        """
        Test return datatype
        """
        actual = self.bot.simulate_move("red", 1, self.game.board)
        self.assertIsInstance(actual, tuple)
        self.assertIsInstance(actual[0], list)
        self.assertTrue(all(isinstance(row, list) for row in actual[0]))
        self.assertIsInstance(actual[1], str)
        self.assertIsInstance(actual[2], str)

    def test_1(self):
        """
        Test a simulation for the given camel, roll, and game board.
        """
        pass

    # Test EVBot.calculate_ev
    def test_2(self):
        """
        Test return datatype
        """
        actual = self.bot.calculate_ev()
        self.assertIsInstance(actual, str)

    def test_3(self):
        """
        Test EV calculations for all camels.

        NOTE: Implicitly tests find_simulated_winner as well.
        """
        pass

    def test_4(self):
        """
        Test EV calculations for all camels.

        NOTE: Implicitly tests find_simulated_winner as well.
        """
        pass

    def test_5(self):
        """
        Test EV calculations for all camels.

        NOTE: Implicitly tests find_simulated_winner as well.
        """
        pass

    def test_6(self):
        """
        Test EV calculations with the edge case that there
        are no remaining betting cards for some colors.
        """
        pass


class TestGameManager(unittest.TestCase):
    """
    Unit test cases for the GameManager class.
    """

    def setUp(self) -> None:
        self.game_manager = GameManager(Player("Alice"), Player("Bob"))
        self.game_manager.winning_camel = "red"
        self.game_manager.second_camel = "green"
        self.game_manager.board = [[] for _ in range(16)]

    # Test GameManager.update_score with simulated bets
    def test_0(self):
        """
        Player 1 bets 5 on the winning camel.
        """
        self.game_manager.players[0].cards["red"] = [5]
        self.game_manager.update_score()
        self.assertEqual(self.game_manager.player_scores[0], 8)

    def test_1(self):
        """
        Player 1 bets 5 on the runner-up camel.
        """
        self.game_manager.players[0].cards["green"] = [5]
        self.game_manager.update_score()
        self.assertEqual(self.game_manager.player_scores[0], 4)

    def test_2(self):
        """
        Player 1 bets 5 and 3 on the winning camel.
        """
        self.game_manager.players[0].cards["red"] = [5, 3]
        self.game_manager.update_score()
        self.assertEqual(self.game_manager.player_scores[0], 11)

    def test_3(self):
        """
        Players 1 and 2 bet all the cards for the winning camel.
        """
        self.game_manager.players[0].cards["red"] = [5, 3]
        self.game_manager.players[1].cards["red"] = [3, 2]
        self.game_manager.update_score()
        self.assertEqual(self.game_manager.player_scores[0], 11)
        self.assertEqual(self.game_manager.player_scores[1], 8)

    def test_4(self):
        """
        Player 1 bets on varying cards for both winning camels.
        """
        self.game_manager.players[0].cards["red"] = [5, 3, 3]
        self.game_manager.players[0].cards["green"] = [5, 3, 3]
        self.game_manager.update_score()
        self.assertEqual(self.game_manager.player_scores[0], 17)

    def test_5(self):
        """
        Players 1 and 2 bet on varying cards for both winning camels.

        NOTE: 1 point is subtracted for every incorrect bet!
        """
        self.game_manager.players[0].cards["red"] = [5, 3]
        self.game_manager.players[1].cards["green"] = [5, 3]
        self.game_manager.players[0].cards["blue"] = [5, 3, 3]
        self.game_manager.players[1].cards["red"] = [3, 2]
        self.game_manager.update_score()
        self.assertEqual(self.game_manager.player_scores[0], 8)
        self.assertEqual(self.game_manager.player_scores[1], 10)

    # Test GameManager.init_camels
    def test_6(self):
        """
        Test return datatype.
        """
        self.assertIsInstance(self.game_manager.init_camels(), list)
        self.assertTrue(
            all(isinstance(item, list) for item in self.game_manager.init_camels())
        )

    def test_7(self):
        """
        The initialized board should not be blank.
        """
        self.assertTrue(
            deepcopy(self.game_manager.board) != self.game_manager.init_camels()
        )

    def test_8(self):
        """
        After initialization, all camels should exist within the board.
        """
        self.game_manager.init_camels()
        self.assertTrue(
            all(
                [
                    any([camel in stack for stack in self.game_manager.board])
                    for camel in ["red", "green", "blue", "yellow", "purple"]
                ]
            )
        )

    # Test GameManager.move_camels with varying board states
    def test_9(self):
        """
        Test that the board is no longer blank after a move.
        """
        self.game_manager.board[0].append("red")
        self.game_manager.move_camels("red", 8)
        self.assertTrue(self.game_manager.board != [[] for _ in range(16)])

    def test_10(self):
        """
        Test the movement of individual camels.
        """
        self.game_manager.board[0].append("red")
        self.game_manager.move_camels("red", 3)
        self.assertListEqual(self.game_manager.board[3], ["red"])

    def test_11(self):
        """
        Test the movement of stacked camels.
        """
        self.game_manager.board[0].extend(["red", "green"])
        self.game_manager.move_camels("red", 3)
        self.assertListEqual(self.game_manager.board[3], ["red", "green"])

    def test_12(self):
        """
        Test that winning_camel is initialized when a camel passes the finish line.
        """
        self.game_manager.winning_camel = None
        self.game_manager.board[14].append("red")
        self.game_manager.move_camels("red", 3)
        self.assertIsNotNone(self.game_manager.winning_camel)

    def test_13(self):
        """
        Test that second_camel is also initialized when a camel passes the finish line.
        """
        self.game_manager.winning_camel = None
        self.game_manager.second_camel = None
        self.game_manager.board[14].extend(["red", "green"])
        self.game_manager.move_camels("red", 3)
        self.assertIsNotNone(self.game_manager.winning_camel)
        self.assertIsNotNone(self.game_manager.second_camel)

    def test_14(self):
        """
        Test that the winning camel is the right one.
        """
        self.game_manager.board[14].append("red")
        self.game_manager.move_camels("red", 3)
        self.assertEqual(self.game_manager.winning_camel, "RED")

    def test_15(self):
        """
        Test that the second camel is the right one.
        """
        self.game_manager.board[14].extend(["red", "green"])
        self.game_manager.move_camels("red", 3)
        self.assertEqual(self.game_manager.second_camel, "RED")

    def test_16(self):
        """
        Test that the function works when the second camel doesn't cross the finish line.
        """
        self.game_manager.board[14].append("red")
        self.game_manager.board[10].append("green")
        self.game_manager.move_camels("red", 3)
        self.assertEqual(self.game_manager.second_camel, "GREEN")

    # Test GameManager.leg_reset
    def test_17(self):
        """
        Ensure variables are reset to their original states (except self.game.current_player)
        """
        # Modify game state
        self.game_manager.cards = {
            color: [1, 1, 1, 1]
            for color in ["red", "green", "blue", "yellow", "purple"]
        }
        self.game_manager.dice = {
            color: 1 for color in ["red", "green", "blue", "yellow", "purple"]
        }
        self.game_manager.players[0].cards["red"] = [5, 3, 2, 2]
        self.game_manager.players[1].cards["blue"] = [5, 3, 2, 2]

        # Capture current player
        current_player = self.game_manager.current_player

        # Perform leg reset
        self.game_manager.leg_reset()

        # Check if cards, dice, and player bets are reset correctly
        self.assertEqual(
            self.game_manager.cards,
            {
                color: [5, 3, 2, 2]
                for color in ["red", "green", "blue", "yellow", "purple"]
            },
        )
        self.assertEqual(
            self.game_manager.dice,
            {color: 0 for color in ["red", "green", "blue", "yellow", "purple"]},
        )
        for player in self.game_manager.players:
            self.assertEqual(
                player.cards,
                {color: [] for color in ["red", "green", "blue", "yellow", "purple"]},
            )

    def test_18(self):
        """
        Test that the first player for the next leg is the player not currently playing.
        """
        # Set initial player
        initial_player = self.game_manager.current_player

        # Perform leg reset
        self.game_manager.leg_reset()

        # Check if current player is switched to the other player
        expected_player = (
            self.game_manager.players[1]
            if initial_player == self.game_manager.players[0]
            else self.game_manager.players[0]
        )
        self.assertEqual(self.game_manager.current_player, expected_player)


if __name__ == "__main__":
    unittest.main()
