import random


class Player:
    def __init__(self):
        self.coins = 3
        self.cards = {"red": [], "green": [], "blue": [], "yellow": [], "purple": []}

    def roll(self, dice: list) -> tuple:
        pick = random.choice(dice)
        return (pick, random.choice([1, 2, 3])) if bool(dice) else ()

    def take_bet(self):
        pass
