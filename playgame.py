from gamemanager import GameManager
from evbot import EVBot
import colorama
import os


class PlayGame:
    """
    Manages the display and player actions
    """

    def __init__(self, game_manager: GameManager):
        """
        Initialize the PlayGame class.

        Args:
            game_manager (GameManager): The game manager for the game.
        """
        self.manager = game_manager
        self.current_player = game_manager.current_player
        self.current_name = game_manager.player_names[0]
        self.color_dict = {
            "RED": colorama.Fore.RED,
            "GREEN": colorama.Fore.GREEN,
            "BLUE": colorama.Fore.BLUE,
            "YELLOW": colorama.Fore.YELLOW,
            "PURPLE": colorama.Fore.MAGENTA,
        }
        self.num_dice_rolled = 0
        self.leg_winner = ""
        self.leg_second = "" 
        colorama.init(autoreset=True)

    def clear(self) -> None:
        """
        Clear the console screen.
        """
        os.system("cls" if os.name == "nt" else "clear")

    def take_turn(self, action = None, color = None) -> None:
        """
        Handle the player's turn by getting the player's action and executing it.
        """
        if not action:
            action = self.get_player_action()
        if action == "B":
            self.handle_bet(color)
        elif action == "R":
            self.handle_roll()
        else:
            self.handle_hint()
            self.take_turn()
        self.switch_turn()

    def get_player_action(self) -> str:
        """
        Prompt the player to choose an action (Bet, Roll, Hint).

        Returns:
            str: The action
        """
        while True:
            action = input(f"\n{self.current_name}'s turn!\n(B)et, (R)oll, or get (H)int? ").upper()
            if action in ["B", "BET"]:
                return "B"
            elif action in ["R", "ROLL"]:
                return "R"
            elif action in ["H", "Hint"]:
                return "H"
            else:
                print("Sorry, that's not a valid move.")

    def handle_bet(self, color = None) -> None:
        """
        Handle the bet action by prompting the player to choose a bet color.
        """
        if not color:
            color = self.get_bet_color()
        self.manager.cards = self.current_player.take_bet(color, self.manager.cards)

    def get_bet_color(self) -> str:
        """
        Prompt the player to choose a bet color.

        Returns:
            str: The bet color
        """
        camel_colors = ["red", "green", "blue", "yellow", "purple"]
        camel_short = ["r", "g", "b", "y", "p"]
        while True:
            color = input(
                "Which bet would you like to place? (red, green, blue, yellow, purple) "
            ).lower()
            if color in camel_short:
                color = camel_colors[camel_short.index(color)]
                if len(self.manager.cards[color]) != 0:
                    return color
                else:
                    print(f"Sorry, all the {color} cards are gone.")
            elif color in camel_colors:
                if len(self.manager.cards[color]) != 0:
                    return color
                else:
                    print(f"Sorry, all the {color} cards are gone.")
            else:
                print("Sorry, that's not a valid card.")

    def handle_roll(self) -> None:
        """
        Handle the roll action by rolling available dice and moving camels accordingly.
        """
        available_dice = [key for key in self.manager.dice if self.manager.dice[key] == 0]
        color, number = self.current_player.roll(available_dice)
        self.manager.dice[color] = number
        self.num_dice_rolled += 1
        self.manager.move_camels(color, number)
    
    def handle_hint(self) -> None:
        self.current_player.coins -= 1
        print(EVBot(self.manager).calculate_ev())

    def switch_turn(self) -> None:
        """
        Switch the turn to the other player.
        """
        self.current_player = (
            self.manager.players[1]
            if self.current_player == self.manager.players[0]
            else self.manager.players[0]
        )
        self.current_name = (
            self.manager.player_names[1]
            if self.current_name == self.manager.player_names[0]
            else self.manager.player_names[0]
        )

    def display_game(self) -> None:
        """
        Display the current state of the game.
        """
        self.clear()
        print(self.get_game_state())

    def get_game_state(self) -> str:
        """
        Get the current game state.

        Returns:
            str: The current game state as a formatted string.
        """
        game_state = []
        game_state.append(self.get_ticket_tents_state())
        game_state.append(self.get_dice_tents_state())
        game_state.append(self.get_board_state())
        game_state.append(self.get_board_positions())
        game_state.append(self.get_player_info())
        return "".join(game_state)

    def get_ticket_tents_state(self) -> str:
        """
        Get the current ticket tents state.

        Returns:
            str: The current ticket tents state as a formatted string.
        """
        state = ["   Ticket Tents: "]
        for key in ["red", "green", "blue", "yellow", "purple"]:
            if len(self.manager.cards[key]) != 0:
                state.append(
                    self.color_dict[key.upper()] + str(max(self.manager.cards[key])) + " "
                )
            else:
                state.append(self.color_dict[key.upper()] + "X ")
        state.append(" " * 10)
        return "".join(state)

    def get_dice_tents_state(self) -> str:
        """
        Get the current dice tents state.

        Returns:
            str: The dice tents state as a formatted string.
        """
        state = [colorama.Fore.WHITE + "Dice Tents: "]
        for die in ["red", "green", "blue", "yellow", "purple"]:
            if self.manager.dice[die] != 0:
                state.append(
                    self.color_dict[die.upper()] + str(self.manager.dice[die]) + " "
                )
            else:
                state.append(self.color_dict[die.upper()] + "_ ")
        state.append("\n\n")
        return "".join(state)

    def get_board_state(self) -> str:
        """
        Get the current board state.

        Returns:
            str: The current board state as a formatted string.
        """
        state = []
        for row in range(4, -1, -1):
            state.append("🌴  ")
            for pos in range(16):
                if len(self.manager.board[pos]) > row:
                    camel = self.manager.board[pos][row]
                    if len(camel) != 0:
                        if pos <= 8:
                            state.append(
                                self.color_dict[camel.upper()]
                                + camel[0][0].upper()
                                + "  "
                            )
                        else:
                            state.append(
                                self.color_dict[camel.upper()]
                                + camel[0][0].upper()
                                + "   "
                            )
                elif pos <= 8:
                    state.append("   ")
                else:
                    state.append("    ")
            state.append("🏁\n")
        return "".join(state)

    def get_board_positions(self) -> str:
        """
        Get the current board positions.

        Returns:
            str: The current board positions as a formatted string.
        """
        state = ["    " + colorama.Fore.WHITE]
        for i in range(1, 17):
            state.append(str(i) + "  ")
        state.append("\n\n")
        return "".join(state)

    def get_player_info(self) -> str:
        """
        Get the players' current information.

        Returns:
            str: The players' current information as a formatted string.
        """
        state = ["   "]
        spacer = 0
        if self.manager.players[0].coins > 9:
            spacer = 1
        state.append(
            f"{self.manager.player_names[0]} has {self.manager.players[0].coins} coins."
            + " " * (22 - spacer)
        )
        state.append(
            f"{self.manager.player_names[1]} has {self.manager.players[1].coins} coins.\n"
        )

        state.append(self.get_player_bets(0, "   "))
        state.append(self.get_player_bets(1, " "))

        return "".join(state)

    def get_player_bets(self, player_index: int, padding: str) -> str:
        """
        Get the bets of a player for the current leg.

        Args:
            player_index (int): The index of the player
            padding (str): The padding for the bets display

        Returns:
            str: The bets of a player for the current leg as a formatted string.
        """
        state = [colorama.Fore.WHITE + padding + "Bets: "]
        count = 0
        for key in self.manager.players[player_index].cards:
            for i in self.manager.players[player_index].cards[key]:
                state.append(self.color_dict[key.upper()] + str(i) + " ")
                count += 1
        if player_index == 0:
            state.append(" " * (33 - 2 * count))
        return "".join(state)

    def display_leg_results(self, og_coins: list) -> None:
        """
        Display the results of the leg when all dice have been rolled.
        """
        self.clear()
        leg_ended = ["\n\n", self.get_board_state(), self.get_board_positions()]
        leg_ended.append(" " * 25 + "LEG ENDED!\nLeg Results:\n")
        leg_ended.append(self.get_leg_places())
        leg_ended.append(self.get_player_scores_update(og_coins))
        print("".join(leg_ended))
        input("Press ENTER to continue... ")

    def get_leg_places(self) -> str:
        """
        Get the camel positions for the leg.

        Returns:
            str: The camel positions for the leg as a formatted string.
        """
        leg_places = []
        leg_places.append(
            colorama.Fore.WHITE
            + "🥇 FIRST PLACE 🥇: "
            + self.color_dict[self.leg_winner.upper()]
            + self.leg_winner.upper()
            + colorama.Fore.WHITE
            + "\n"
        )
        leg_places.append(
            colorama.Fore.WHITE
            + "🥈 SECOND PLACE 🥈: "
            + self.color_dict[self.leg_second.upper()]
            + self.leg_second.upper()
            + "\n"
        )
        return "".join(leg_places)

    def get_player_scores_update(self, og_coins: list) -> str:
        """
        Update and get the players' scores for the leg.

        Returns:
            str: The formatted string of the players' updated scores for the leg.
        """
        self.manager.update_score()
        self.manager.players[0].coins = self.manager.player_scores[0]
        self.manager.players[1].coins = self.manager.player_scores[1]

        spacer = 0
        if self.manager.player_scores[0] > 9:
            spacer += 1
        if abs(self.manager.player_scores[0] - og_coins[0]) > 9:
            spacer += 1
        if self.manager.player_scores[0] - og_coins[0] < 0:
            spacer += 1

        player_scores = [colorama.Fore.WHITE]
        player_scores.append(
            f"{self.manager.player_names[0]} has {self.manager.player_scores[0]} coins ({self.manager.player_scores[0] - og_coins[0]} coins)."
            + " " * (13 - spacer)
            + "\n"
        )
        player_scores.append(
            f"{self.manager.player_names[1]} has {self.manager.player_scores[1]} coins ({self.manager.player_scores[1] - og_coins[1]} coins).\n"
        )

        return "".join(player_scores)

    def calculate_leg_winners(self) -> None:
        """
        Calculate the winners based on the camel positions on the board.
        """
        winning_camel_found = False
        for i in range(15, 0, -1):
            if len(self.manager.board[i]) > 0:
                if not winning_camel_found:
                    self.leg_winner = self.manager.board[i][-1]
                    winning_camel_found = True
                else:
                    self.leg_second = self.manager.board[i][-1]
                    break

    def game_over(self) -> None:
        """
        Display the winner of the game.
        """
        self.clear()
        self.manager.update_score()
        player1_score = self.manager.player_scores[0]
        player2_score = self.manager.player_scores[1]

        if player1_score > player2_score:
            winner = self.manager.players[0]
            second = self.manager.players[1]
        else:
            winner = self.manager.players[1]
            second = self.manager.players[0]

        game_over = [
            "\n\n",
            self.get_board_state(),
            self.get_board_positions(),
            colorama.Fore.WHITE + "GAME OVER!\n",
            f"The winning camel was {self.color_dict[self.manager.winning_camel] + self.manager.winning_camel + colorama.Fore.WHITE} and the runner up camel was {self.color_dict[self.manager.second_camel] + self.manager.second_camel + colorama.Fore.WHITE}!\n",
            f"{winner.name} WINS with {winner.coins} coins!\n",
            f"{second.name} came in second with {second.coins} coins.\n",
        ]
        print("".join(game_over))
        print("Thanks for playing Camel Up!")
