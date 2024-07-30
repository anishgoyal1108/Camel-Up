from player import Player
import random


class GameManager:
    def __init__(self, Player1=Player(), Player2=Player()):
        self.cards = {
            "red": [5, 3, 2, 2],
            "green": [5, 3, 2, 2],
            "blue": [5, 3, 2, 2],
            "yellow": [5, 3, 2, 2],
            "purple": [5, 3, 2, 2],
        }
        self.dice = ["red", "green", "blue", "yellow", "purple"]
        self.current_player = Player1
        self.board = [[] for _ in range(16)]

        self.player_scores = [0, 0]
        self.winning_camel = ""
        self.second_camel = ""
        self.players = [Player1, Player2]

    def init_camels(self) -> None:
        dice = ["red", "green", "blue", "yellow", "purple"]
        for _ in range(5):
            pick = random.choice(dice)
            dice.remove(pick)
            position = random.choice([0, 1, 2])
            self.board[position].append(pick)

    def move_camels(self, camel: str, roll: int) -> None:
        camel_position = 0
        moving_camels = []
        for i in range(16):
            if camel in self.board[i]:
                camel_position = i
                camel_index = self.board[i].index(camel)
                moving_camels = self.board[i][:camel_index:]
                
                break
        print(self.board.index(camel))
        pass

    def display_game(self):
        pass

    def update_score(self) -> None:
        for p in range(2):
            for camel in self.players[p].cards:
                if camel == self.winning_camel:
                    for card in self.players[p].cards[self.winning_camel]:
                        self.player_scores[p] += card
                elif camel == self.second_camel:
                    for card in self.players[p].cards[self.second_camel]:
                        self.player_scores[p] += 1
                else:
                    for card in self.players[p].cards[camel]:
                        self.player_scores[p] -= 1

    def display_stats(self):
        pass