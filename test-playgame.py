import unittest
from playgame import PlayGame
from gamemanager import GameManager
from player import Player

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
        self.assertEqual(len([key for key in game.manager.dice if game.manager.dice[key] == 0]), 4)
        self.assertEqual(game.num_dice_rolled, 1)
        game.take_turn("R")
        self.assertEqual(game.current_player.name, "Alice")
        self.assertEqual(bob.coins, 4)
        self.assertEqual(len([key for key in game.manager.dice if game.manager.dice[key] == 0]), 3)
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
        self.assertRaises(IndexError, game.take_turn("B", "red"))

    def test_3(self):
        """
        Test getting hint for a player's turn.
        """
        pass
    
    def test_4(self):
       pass 


if __name__ == "__main__":
    unittest.main()