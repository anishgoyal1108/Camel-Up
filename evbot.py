from gamemanager import GameManager
from itertools import permutations, product
from copy import deepcopy


class EVBot:
    """
    A bot that calculates the expected value (EV) of bets in a camel racing game using Monte Carlo simulations.
    """

    def __init__(self, game: GameManager):
        """
        Initializes the EVBot with a given game state.

        Args:
            game (GameManager): The game manager instance containing the current game state.
        """
        self.game = game
        self.outcomes = [1, 2, 3]

    def simulate_move(
        self, camel: str, roll: int, board: list[list]
    ) -> tuple[list[list], str, str]:
        """
        Simulates a move for a given camel and roll on the game board.

        Args:
            camel (str): The camel to move.
            roll (int): The number of spaces the camel moves.
            board (list[list]): The current state of the game board.
        Returns:
            tuple[list[list], str, str]: A tuple containing the new game board, the winning camel, and the second camel.
        """
        board_copy = deepcopy(board)
        for i, stack in enumerate(board_copy):
            if camel in stack:
                camel_index = stack.index(camel)
                moving_camels = stack[camel_index:]
                board_copy[i] = stack[:camel_index]
                if i + roll >= len(board_copy):
                    winning_camel = moving_camels[-1]
                    if len(moving_camels) > 1:
                        second_camel = moving_camels[-2]
                        return board_copy, winning_camel, second_camel
                    for stack in reversed(board_copy[:-1]):
                        if stack:
                            second_camel = stack[-1]
                            return board_copy, winning_camel, second_camel
                else:
                    board_copy[i + roll].extend(moving_camels)
        return board_copy, "", ""

    def find_simulated_winner(self, board: list[list]) -> tuple[str, str]:
        """
        Determines the winning and second camel from the simulated board state.

        Args:
            board (list[list]): The simulated game board.
        Returns:
            tuple[str, str]: A tuple containing the winning camel and the second camel.
        """
        for i in range(15, 0, -1):
            if board[i]:
                winning_camel = board[i][-1]
                for j in range(i - 1, 0, -1):
                    if board[j]:
                        return winning_camel, board[j][-1]
                return winning_camel, ""
        return "", ""

    def calculate_ev(self) -> str:
        """
        Calculates the expected value (EV) of bets for each camel based on simulated game outcomes.

        Returns:
            str: A string describing the EV, probability of winning, and probability of being runner-up for each camel,
                along with a recommendation for which camel to bet on.
        """
        available_dice = [key for key in self.game.dice if self.game.dice[key] == 0]
        win_counts = {color: 0 for color in self.game.colors}
        second_counts = {color: 0 for color in self.game.colors}
        camel_roll_orders = list(permutations(available_dice))
        combinations = list(product(self.outcomes, repeat=len(available_dice)))

        for order in camel_roll_orders:
            for combo in combinations:
                game_board_copy = deepcopy(self.game.board)
                for i in range(len(combo)):
                    game_board_copy, winning_camel, second_camel = self.simulate_move(
                        order[i], combo[i], game_board_copy
                    )
                    if winning_camel:
                        break
                if not winning_camel:
                    winning_camel, second_camel = self.find_simulated_winner(
                        game_board_copy
                    )
                win_counts[winning_camel] += 1
                second_counts[second_camel] += 1

        total_outcomes = len(camel_roll_orders) * len(combinations)
        ev_values = {color: 0 for color in self.game.colors}
        max_ev, max_ev_camel = -1, None
        ev_values_string = []

        for color in win_counts:
            prob_win = win_counts[color] / total_outcomes
            prob_second = second_counts[color] / total_outcomes
            not_1st_or_2nd = 1 - (
                (win_counts[color] + second_counts[color]) / total_outcomes
            )
            if color in self.game.cards and self.game.cards[color]:
                ev_values[color] = (
                    prob_win * self.game.cards[color][0] + prob_second - not_1st_or_2nd
                )
                if max_ev_camel is None or ev_values[color] > max_ev:
                    max_ev, max_ev_camel = ev_values[color], color
            else:
                ev_values_string.append(f"{color} - Betting not applicable!\n")
                continue

            ev_values_string.append(
                f"{color} - P(Winning): {prob_win:.2f}    P(Runner-Up): {prob_second:.2f}    EV: {ev_values[color]:.2f}\n"
            )

        ev_values_string.append(f"\nYou should bet on {max_ev_camel}.")
        return "".join(ev_values_string)
