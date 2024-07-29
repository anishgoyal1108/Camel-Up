from gamemanager import GameManager
import random


class Player:
    def __init__(self):
        self.coins = 3
        self.cards = {"red": [], "green": [], "blue": [], "yellow": [], "purple": []}

    def roll(self, gm: GameManager) -> tuple:
        pick = random.choice(gm.dice)
        gm.dice.remove(pick)
        return (pick, random.choice([1, 2, 3])) if bool(self.dice) else ()

    def take_bet(self, gm: GameManager):
        pass
