from player import Player
import random


class GameManager:
    """
    Manages the state and rules of Camel Up.
    """

    def __init__(self, Player1, Player2):
        """
        Initialize the GameManager with players and game state.

        Args:
            Player1 (Player): The first player.
            Player2 (Player): The second player.
        """
        self.colors = ["red", "green", "blue", "yellow", "purple"]
        self.cards = {color: [5, 3, 2, 2] for color in self.colors}
        self.dice = {color: 0 for color in self.colors}
        self.current_player = Player1
        self.board = [[] for _ in range(16)]
        self.player_scores = [0, 0]
        self.winning_camel = ""
        self.second_camel = ""
        self.players = [Player1, Player2]
        self.player_names = [Player1.name, Player2.name]

    def init_camels(self) -> None:
        """
        Initialize the camels on the board at random positions.
        """
        dice = self.colors.copy()
        for _ in range(5):
            pick = random.choice(dice)
            dice.remove(pick)
            position = random.choice([0, 1, 2])
            self.board[position].append(pick)

    def move_camels(self, camel: str, roll: int) -> None:
        """
        Move the camels on the board according to the roll.

        Args:
            camel (str): The color of the camel to move.
            roll (int): The number of spaces to move the camel.
        """
        camel_long = [color.upper() for color in self.colors]
        camel_short = [color[0] for color in camel_long]
        for i, stack in enumerate(self.board):
            if camel in stack:
                camel_index = stack.index(camel)
                moving_camels = stack[camel_index:]
                self.board[i] = stack[:camel_index]
                if i + roll >= len(self.board):
                    self.winning_camel = camel_long[
                        camel_short.index(moving_camels[-1])
                    ]
                    self.second_camel = self.find_second_camel(
                        moving_camels, camel_long, camel_short
                    )
                else:
                    self.board[i + roll].extend(moving_camels)
                break

    def find_second_camel(self, moving_camels, camel_long, camel_short) -> str:
        """
        Helper method to find the second camel in the race.

        Args:
            moving_camels (list): The list of camels being moved.
            camel_long (list): The list of camel colors in long format.
            camel_short (list): The list of camel colors in short format.

        Returns:
            str: The color of the second camel in the race.
        """
        if len(moving_camels) > 1:
            return camel_long[camel_short.index(moving_camels[-2])]
        for stack in reversed(self.board[:-1]):
            if stack:
                return camel_long[camel_short.index(stack[-1])]
        return ""

    def update_score(self) -> None:
        """
        Update the scores of the players based on their bets.
        """
        self.player_scores = [player.coins for player in self.players]

        for p, player in enumerate(self.players):
            for camel, bets in player.cards.items():
                if camel == self.winning_camel:
                    self.player_scores[p] += sum(bets)
                elif camel == self.second_camel:
                    self.player_scores[p] += len(bets)
                else:
                    self.player_scores[p] -= len(bets)

    def leg_reset(self) -> None:
        """
        Reset the leg of the game, including cards, dice, and player bets.
        """
        self.cards = {
            color: [5, 3, 2, 2]
            for color in ["red", "green", "blue", "yellow", "purple"]
        }
        self.dice = {color: 0 for color in ["red", "green", "blue", "yellow", "purple"]}
        self.current_player = (
            self.players[1]
            if self.current_player == self.players[0]
            else self.players[0]
        )
        for player in self.players:
            player.cards = {
                color: [] for color in ["red", "green", "blue", "yellow", "purple"]
            }
