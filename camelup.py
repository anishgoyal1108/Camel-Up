from gamemanager import GameManager
import colorama
import os


class PlayGame:
    """
    Manages the display and player actions
    """

    def __init__(self, game_manager: GameManager):
        """
        Initialize the PlayGame class.
        """
        self.game = game_manager
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
        colorama.init(autoreset=True)

    def clear(self) -> None:
        """
        Clear the console screen.
        """
        os.system("cls" if os.name == "nt" else "clear")

    def take_turn(self) -> None:
        """
        Handle the player's turn by getting the player's action and executing it.
        """
        action = self.get_player_action()
        if action == "B":
            self.handle_bet()
        else:
            self.handle_roll()
        self.switch_turn()
        if self.num_dice_rolled == 5:
            self.display_leg_results()
            self.num_dice_rolled = 0
            self.game.leg_reset()

    def get_player_action(self) -> str:
        """
        Prompt the player to choose an action (Bet or Roll).
        """
        while True:
            action = input(f"\n{self.current_name}'s turn!\n(B)et or (R)oll? ").upper()
            if action in ["B", "BET"]:
                return "B"
            elif action in ["R", "ROLL"]:
                return "R"
            else:
                print("Sorry, that's not a valid move.")

    def handle_bet(self) -> None:
        """
        Handle the bet action by prompting the player to choose a bet color.
        """
        color = self.get_bet_color()
        self.game.cards = self.current_player.take_bet(color, self.game.cards)

    def get_bet_color(self) -> str:
        """
        Prompt the player to choose a bet color.
        """
        camel_colors = ["red", "green", "blue", "yellow", "purple"]
        camel_short = ["r", "g", "b", "y", "p"]
        while True:
            color = input(
                "Which bet would you like to place? (red, green, blue, yellow, purple) "
            ).lower()
            if color in camel_short:
                color = camel_colors[camel_short.index(color)]
                if len(self.game.cards[color]) != 0:
                    return color
                else:
                    print(f"Sorry, all the {color} cards are gone.")
            elif color in camel_colors:
                if len(self.game.cards[color]) != 0:
                    return color
                else:
                    print(f"Sorry, all the {color} cards are gone.")
            else:
                print("Sorry, that's not a valid card.")

    def handle_roll(self) -> None:
        """
        Handle the roll action by rolling available dice and moving camels accordingly.
        """
        available_dice = [key for key in self.game.dice if self.game.dice[key] == 0]
        color, number = self.current_player.roll(available_dice)
        self.game.dice[color] = number
        self.num_dice_rolled += 1
        self.game.move_camels(color, number)

    def switch_turn(self) -> None:
        """
        Switch the turn to the other player.
        """
        self.current_player = (
            self.game.players[1]
            if self.current_player == self.game.players[0]
            else self.game.players[0]
        )
        self.current_name = (
            self.game.player_names[1]
            if self.current_name == self.game.player_names[0]
            else self.game.player_names[0]
        )

    def display_game(self) -> None:
        """
        Display the current state of the game.
        """
        self.clear()
        print(self.get_game_state())

    def get_game_state(self) -> str:
        """
        Get the current game state as a formatted string.
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
        Get the ticket tents state as a formatted string.
        """
        state = ["   Ticket Tents: "]
        for key in ["red", "green", "blue", "yellow", "purple"]:
            if len(self.game.cards[key]) != 0:
                state.append(
                    self.color_dict[key.upper()] + str(max(self.game.cards[key])) + " "
                )
            else:
                state.append(self.color_dict[key.upper()] + "X ")
        state.append(" " * 10)
        return "".join(state)

    def get_dice_tents_state(self) -> str:
        """
        Get the dice tents state as a formatted string.
        """
        state = [colorama.Fore.WHITE + "Dice Tents: "]
        for die in ["red", "green", "blue", "yellow", "purple"]:
            if self.game.dice[die] != 0:
                state.append(
                    self.color_dict[die.upper()] + str(self.game.dice[die]) + " "
                )
            else:
                state.append(self.color_dict[die.upper()] + "_ ")
        state.append("\n\n")
        return "".join(state)

    def get_board_state(self) -> str:
        """
        Get the board state as a formatted string.
        """
        state = []
        for row in range(4, -1, -1):
            state.append("🌴  ")
            for pos in range(16):
                if len(self.game.board[pos]) > row:
                    camel = self.game.board[pos][row]
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
        Get the board positions as a formatted string.
        """
        state = ["    " + colorama.Fore.WHITE]
        for i in range(1, 17):
            state.append(str(i) + "  ")
        state.append("\n\n")
        return "".join(state)

    def get_player_info(self) -> str:
        """
        Get the players' information as a formatted string.
        """
        state = ["   "]
        spacer = 0
        if self.game.players[0].coins > 9:
            spacer = 1
        state.append(
            f"{self.game.player_names[0]} has {self.game.players[0].coins} coins."
            + " " * (22 - spacer)
        )
        state.append(
            f"{self.game.player_names[1]} has {self.game.players[1].coins} coins.\n"
        )

        state.append(self.get_player_bets(0, "   "))
        state.append(self.get_player_bets(1, " "))

        return "".join(state)

    def get_player_bets(self, player_index: int, padding: str) -> str:
        """
        Get the bets of a player as a formatted string.
        """
        state = [colorama.Fore.WHITE + padding + "Bets: "]
        count = 0
        for key in self.game.players[player_index].cards:
            for i in self.game.players[player_index].cards[key]:
                state.append(self.color_dict[key.upper()] + str(i) + " ")
                count += 1
        if player_index == 0:
            state.append(" " * (33 - 2 * count))
        return "".join(state)

    def display_leg_results(self) -> None:
        """
        Display the results of the leg when all dice have been rolled.
        """
        leg_ended = []
        leg_ended.append(" " * 34 + "LEG ENDED!\nLeg Results:\n")
        leg_ended.append(self.get_leg_places())
        leg_ended.append(self.get_player_scores_update())
        print("".join(leg_ended))
        input("Press any key to continue... ")

    def get_leg_places(self) -> str:
        """
        Get the formatted string of the camel positions for the leg.
        """
        leg_places = []
        leg_places.append(
            "🥇 FIRST PLACE 🥇: "
            + self.color_dict[self.game.winning_camel.upper()]
            + self.game.winning_camel.upper()
            + "\n"
        )
        leg_places.append(
            "🥈 SECOND PLACE 🥈: "
            + self.color_dict[self.game.second_camel.upper()]
            + self.game.second_camel.upper()
            + "\n"
        )
        return "".join(leg_places)

    def get_player_scores_update(self) -> str:
        """
        Get the formatted string of the player scores update for the leg.
        """
        init_player1_coins = self.game.players[0].coins
        init_player2_coins = self.game.players[1].coins
        self.game.update_score()
        self.game.players[0].coins = self.game.player_scores[0]
        self.game.players[1].coins = self.game.player_scores[1]

        spacer = 0
        if self.game.player_scores[0] > 9:
            spacer += 1
        if abs(self.game.player_scores[0] - init_player1_coins) > 9:
            spacer += 1
        if self.game.player_scores[0] - init_player1_coins < 0:
            spacer += 1

        player_scores = []
        player_scores.append(
            f"{self.game.player_names[0]} has {self.game.player_scores[0]} coins ({self.game.player_scores[0] - init_player1_coins} coins)."
            + " " * (13 - spacer)
            + "\n"
        )
        player_scores.append(
            f"{self.game.player_names[1]} has {self.game.player_scores[1]} coins ({self.game.player_scores[1] - init_player2_coins} coins).\n"
        )

        return "".join(player_scores)


def main() -> None:
    """
    Main function to initialize and run the game loop.
    """
    game = GameManager()
    play_game = PlayGame(game)
    game.init_camels()
    while game.winning_camel == "":
        play_game.display_game()
        play_game.take_turn()
    play_game.display_final()
    print("End Game")


if __name__ == "__main__":
    main()
