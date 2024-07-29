import random


class Player:
    def __init__(self):
        self.coins = 3
        self.cards = {"red": [], "green": [], "blue": [], "yellow": [], "purple": []}

    def roll(self, dice: list) -> tuple:
        pick = random.choice(dice)
        return (pick, random.choice([1, 2, 3])) if bool(dice) else ()

    def take_bet(self, color: str, cards: dict) -> dict:
        cards_copy = cards
        self.cards[color].append(cards[color][0])
        cards_copy[color].pop(0)
        return cards_copy
