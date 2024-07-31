from gamemanager import GameManager
from itertools import permutations, product
from copy import deepcopy

class EVBot:
    def __init__(self, game: GameManager):
        self.game = game
        self.outcomes = [1, 2, 3]
    
    def simulate_move(self, camel: str, roll: int, board: list[list]) -> tuple[list[list], str, str]:
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
        winning_camel_found = False
        winning_camel = ""
        second_camel = ""
        for i in range(15, 0, -1):
            if len(board[i]) > 0:
                if not winning_camel_found:
                    winning_camel = board[i][-1]
                    winning_camel_found = True
                else:
                    second_camel = board[i][-1]
                    break
        return winning_camel, second_camel
    
    def calculate_ev(self) -> str:
        available_dice = [key for key in self.game.dice if self.game.dice[key] == 0]
        win_counts = {"red": 0, "green": 0, "blue": 0, "yellow": 0, "purple": 0}
        second_counts = {"red": 0, "green": 0, "blue": 0, "yellow": 0, "purple": 0}
        camel_roll_orders = list(permutations(available_dice))
        combinations = list(product(self.outcomes, repeat=len(available_dice)))
        for order in camel_roll_orders:
            for combo in combinations:
                game_board_copy = deepcopy(self.game.board)
                winning_camel = ""
                second_camel = ""
                for i in range(len(combo)):
                    game_board_copy, winning_camel, second_camel = self.simulate_move(order[i], combo[i], game_board_copy)
                    if winning_camel != "":
                        break
                if winning_camel == "":
                    winning_camel, second_camel = self.find_simulated_winner()
                win_counts[winning_camel] += 1
                second_counts[second_camel] += 1
        ev_values = {"red": 0, "green": 0, "blue": 0, "yellow": 0, "purple": 0}
        total_num_of_outcomes = len(camel_roll_orders)*len(combinations)
        max_ev = -1
        max_ev_camel = "red"
        ev_values_string = []
        for key in win_counts:
            prob_win = win_counts[key]/total_num_of_outcomes
            prob_second = second_counts[key]/total_num_of_outcomes
            not_1st_or_2nd = 1-((win_counts[key]+second_counts[key])/total_num_of_outcomes)

            ev_values[key] = prob_win*self.game.cards[key][0] + prob_second - not_1st_or_2nd
            if ev_values[key] > max_ev:
                max_ev = ev_values[key]
                max_ev_camel = key
            ev_values_string.append(key + "- Probability of Winning: " + '{0:.2f}'.format(prob_win) + "    Probability of Second: " + '{0:.2f}'.format(prob_second) + "    EV: " + '{0:.2f}'.format(ev_values[key]) + "\n")
        ev_values_string.append(f"\nYou should bet on {max_ev_camel}.")

        return "".join(ev_values_string)