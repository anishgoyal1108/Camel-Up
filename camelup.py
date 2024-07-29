from gamemanager import GameManager
from player import Player
import colorama

class PlayGame:
    def __init__(self, game_manager):
        self.game = game_manager
        self.current_player = game_manager.current_player
    
    def take_turn(self):
        action = input(self.current_player, "take a turn ['roll', 'take card']: ", end=None)
        if (action.lower() == "roll"):
            available_dice = self.game.dice
            self.current_player.roll(available_dice)

if __name__ == "__main__":
    game = GameManager()
