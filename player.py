import random


class Player:
    """
    Represents a player in Camel Up.
    """

    def __init__(self, name: str):
        """
        Initialize a new player with a name, starting coins, and an empty card collection.

        Args:
            name (str): The name of the player.
        """
        self.coins = 3
        self.cards = {"red": [], "green": [], "blue": [], "yellow": [], "purple": []}
        self.name = name

    def roll(self, dice: list) -> tuple:
        """
        Roll a die from the available dice and return the result.
        The player earns 1 coin each time they roll.

        Args:
            dice (list): List of available dice colors.

        Returns:
            tuple: A tuple containing the color of the die rolled and the result of the roll (1, 2, or 3).
                   Returns an empty tuple if no dice are available.
        """
        self.coins += 1
        if not dice:
            return ()

        pick = random.choice(dice)
        roll_result = random.choice([1, 2, 3])
        return (pick, roll_result)

    def take_bet(self, color: str, cards: dict) -> dict:
        """
        Place a bet on a specific color by moving the top card of that color from the provided cards to the player's cards.

        Args:
            color (str): The color of the bet.
            cards (dict): A dictionary of cards available in the game.

        Returns:
            dict: Updated dictionary of cards after the bet has been placed.
        """
        cards_copy = cards.copy()
        self.cards[color].append(cards_copy[color][0])
        cards_copy[color].pop(0)
        return cards_copy