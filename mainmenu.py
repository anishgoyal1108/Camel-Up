from gamemanager import GameManager
from playgame import PlayGame
from player import Player
import colorama
import os


class MainMenu:
    """
    Displays the main menu and handles user choices.
    """

    def __init__(self):
        """
        Initializes the menu
        """
        colorama.init(autoreset=True)
        self.color_dict = {
            "RED": colorama.Fore.RED,
            "GREEN": colorama.Fore.GREEN,
            "BLUE": colorama.Fore.BLUE,
            "YELLOW": colorama.Fore.YELLOW,
            "PURPLE": colorama.Fore.MAGENTA,
            "WHITE": colorama.Fore.WHITE,
        }
        self.logo = """
                                MMMMMMM                     MMMMMMMMMMMMMM
                              MMMMMMMMMMMM                MMMMMMMMMMMMMMMMMMM
                            MMMMMMMMMMMMMMMM                MMMMMMMMMMMMMMMMM
                      MMMMMMMMMMMMMMMMMMMMMM              MMMMMMMMMMMMM   MM
                    MMMMMMMMMMMMMMMMMMMMMMMMMMM            MMMMMMMMMMM
                  MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM        MMMMMMMMMMMM
                MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM    MMMMMMMMMMMMM
                MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
              MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
              MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
              MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
              MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
            MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
            MMMMMMMM  MMMMMMMM  MMMMMMMMMMMMMMMMMMMM
          MMMMM  M   MMMMMMM       MNMMMMMMMMMMMMMM
        MMMMM  MMMM  MMMMMM          MMMMM  MMMMMM
        MMMMMM  MMM  MMMMMM           MMMMM   MMMMM
        MMMMM     M  MMMMM            MMMM     MMMM
        MMMM        MMMMM           MMMMMM      MMMMM
        MMM       MMMMMMM          NMMMMM      MMMMM
        MM         MMMM             MMMM         MMM
        MMMM         MMMM           MMMM           MM
        MMM          MMM           MMM            MMM
        MMMM         MMMM         MMM              MMM
        MMMMM         MMM        MMMM               MMM
          MMMMMM      MMMM        MMMM              MMMMMM
              MMM       MMMMM       MMMM              MMMMMM
                          MMMMM                        MMMMM
                            MMMMM
        """

    def display_menu(self) -> None:
        """
        Display the main menu.
        """
        self.clear()
        print(self.color_dict["YELLOW"] + self.logo)
        print(self.color_dict["WHITE"] + "Welcome to Camel Up!")
        print(self.color_dict["GREEN"] + "1. Start New Game")
        print(self.color_dict["RED"] + "2. Quit")

    def clear(self) -> None:
        """
        Clear the console screen.
        """
        os.system("cls" if os.name == "nt" else "clear")

    def get_user_choice(self) -> int:
        """
        Prompt the user to choose an option.

        Returns:
            int: The user's choice.
        """
        while True:
            choice = input(
                self.color_dict["WHITE"] + "Please enter your choice (1 or 2): "
            )
            if choice.isdigit() and int(choice) in [1, 2]:
                return int(choice)
            print(self.color_dict["RED"] + "Invalid choice. Please enter 1 or 2.")

    def get_player_names(self) -> tuple[str, str]:
        """
        Prompt the user to input names for both players.

        Returns:
            tuple[str, str]: A tuple containing the names for Player 1 and Player 2.
        """
        print(self.color_dict["WHITE"] + "Enter names for both players.")
        player1 = input("Enter name for Player 1 (default 'Alice'): ").strip()
        player2 = input("Enter name for Player 2 (default 'Bob'): ").strip()

        if not player1:
            player1 = "Alice"
        if not player2:
            player2 = "Bob"

        return player1, player2


def main() -> None:
    """
    Main function to initialize and run the game loop.
    """
    menu = MainMenu()

    while True:
        menu.display_menu()
        choice = menu.get_user_choice()

        if choice == 1:
            player1, player2 = menu.get_player_names()
            game = GameManager(Player1=Player(player1), Player2=Player(player2))
            play_game = PlayGame(game)
            game.init_camels()
            og_coins = [game.players[0].coins, game.players[1].coins]
            while game.winning_camel == "":
                play_game.display_game()
                play_game.take_turn()
                if play_game.num_dice_rolled == 5:
                    play_game.num_dice_rolled = 0
                    play_game.calculate_leg_winners()
                    play_game.display_leg_results(og_coins)
                    og_coins = [game.players[0].coins, game.players[1].coins]
                    game.leg_reset()
            print("End Game")
            break

        elif choice == 2:
            print(menu.color_dict["GREEN"] + "Thank you for playing Camel Up!")
            break


if __name__ == "__main__":
    main()
