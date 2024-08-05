from gamemanager import GameManager
from playgame import PlayGame
from player import Player
from mainmenu import MainMenu


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
            while not game.over:
                play_game.display_game()
                play_game.take_turn()
                if play_game.num_dice_rolled == 5:
                    play_game.num_dice_rolled = 0
                    game.calculate_leg_winners()
                    play_game.display_leg_results(og_coins)
                    og_coins = [game.players[0].coins, game.players[1].coins]
                    game.leg_reset()
            play_game.game_over()
            break

        elif choice == 2:
            print(menu.color_dict["GREEN"] + "Thank you for playing Camel Up!")
            break


if __name__ == "__main__":
    main()
