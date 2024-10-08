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
        self.over = False
        self.players = [Player1, Player2]
        self.player_names = [Player1.name, Player2.name]

    def init_camels(self) -> list[list]:
        """
        Initialize the camels on the board at random positions.
        """
        dice = self.colors.copy()
        for _ in range(5):
            pick = random.choice(dice)
            dice.remove(pick)
            position = random.choice([0, 1, 2])
            self.board[position].append(pick)
        return self.board

    def move_camels(self, camel: str, roll: int) -> None:
        """
        Move the camels on the board according to the roll.

        Args:
            camel (str): The color of the camel to move.
            roll (int): The number of spaces to move the camel.
        """
        for i, stack in enumerate(self.board):
            if camel in stack:
                camel_index = stack.index(camel)
                moving_camels = stack[camel_index:]
                self.board[i] = stack[:camel_index]
                if i + roll >= len(self.board):
                    self.over = True
                    self.winning_camel = moving_camels[-1].upper()
                    self.second_camel = (
                        moving_camels[-2].upper()
                        if len(moving_camels) > 1
                        else next(
                            (
                                stack[-1].upper()
                                for stack in reversed(self.board[:-1])
                                if stack
                            ),
                            "",
                        )
                    )
                else:
                    self.board[i + roll].extend(moving_camels)
                    self.calculate_leg_winners()
                break

    def calculate_leg_winners(self) -> None:
        """
        Calculate the winners based on the camel positions on the board.
        """
        winning_camel_found = False
        for i in range(15, 0, -1):
            if len(self.board[i]) > 0:
                if not winning_camel_found:
                    self.winning_camel = self.board[i][-1]
                    winning_camel_found = True
                else:
                    self.second_camel = self.board[i][-1]
                    break

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
