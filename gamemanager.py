from player import Player
import colorama


def GameManager():
    def __init__(self, Player1=Player, Player2=Player):
        self.cards = {
            "red": [5, 3, 2, 2],
            "green": [5, 3, 2, 2],
            "blue": [5, 3, 2, 2],
            "yellow": [5, 3, 2, 2],
            "purple": [5, 3, 2, 2],
        }
        self.dice = ["red", "green", "blue", "yellow", "purple"]
        self.current_player = Player1
        self.board = [[] * 16]

    def play_game(self):
        pass

    def display_game(self):
        pass

    def display_stats(self):
        pass
